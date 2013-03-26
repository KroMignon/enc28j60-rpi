#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     ip.py
# Purpose:  Microchip ENC28J60 Ethernet Interface Driver
#
# Author:   Fabrice MOUSSET
#
# Created:  2013/01/09
# Licence:  GPLv3 or newer
#=============================================================================
# Last commit info:
#
# $LastChangedDate:: xxxx/xx/xx xx:xx:xx $
# $Rev::                                 $
# $Author::                              $
#=============================================================================
# Revision list :
#
# Date       By        Changes
#
#=============================================================================

IP_FRAME_CPT = 0

def set_ip_checksum(buf):
    csum = 0
    # Clear previous Checksum value
    buf[10] = 0
    buf[11] = 0

    # Generate checksum
    for idx in range(len(buf)/2):
        val = buf[idx*2] * 256 + buf[idx*2+1]
        csum += val

    csum = ((csum >> 16) & 0xFFFF) + (csum & 0xFFFF)
    csum += (csum >> 16)
    csum = ~csum

    # Update checksum value in frame
    buf[10] = (csum >> 8) & 0xff
    buf[11] = csum  & 0xff

def make_ip_frame(src, dst, payload):
    size = len(payload)
    buf = [0x45, 0x00, (size >> 8) & 0xff, size & 0xff]
    buf.extend([(IP_FRAME_CPT >> 8) & 0xff, IP_FRAME_CPT & 0xFF])
    IP_FRAME_CPT = (IP_FRAME_CPT + 1) & 0xffff
    buf.extend([0x40, 0, 0, 0])
    buf.extend([int(m) for m in src.split('.')])
    buf.extend([int(m) for m in dst.split('.')])
    set_ip_checksum(buf)
    buf.extend(payload)
    return buf

class IpFrame(object):
    '''
    Decodeur de trame IP (cf. RFC791)

         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |Version|  IHL  |Type of Service|          Total Length         |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |         Identification        |Flags|      Fragment Offset    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |  Time to Live |    Protocol   |         Header Checksum       |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                       Source Address                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                    Destination Address                        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                    Options                    |    Padding    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    '''

    def __init__(self, framebuffer):
        '''
        Constructor
        '''
        self.__framebuffer = framebuffer
        self.__version = framebuffer[0]>>4 & 0x0f
        self.__HLEN = framebuffer[0] & 0x0f
        self.__ToF = framebuffer[1]
        self.__totalLength = framebuffer[2] * 256 + framebuffer[3]
        self.__ID = framebuffer[4] * 255 + framebuffer[5]
        self.__flags = framebuffer[6] >> 5 & 0x03
        self.__offset = (framebuffer[6] & 0x3F) * 256 + framebuffer[7]
        self.__TTL = framebuffer[8]
        self.__protocol = framebuffer[9]
        self.__headerCS = framebuffer[10] * 256 + framebuffer[11]
        self.__srcAddr = ".".join('%d' % framebuffer[12+idx] for idx in range(4))
        self.__destAddr = ".".join('%d' % framebuffer[16+idx] for idx in range(4))
        self.__option = [framebuffer[20 + idx] for idx in range(self.__totalLength - 20)]

    @property
    def isICMP(self):
        return bool(self.__protocol == 1)

    @property
    def isIGMP(self):
        return bool(self.__protocol == 2)

    @property
    def isTCP(self):
        return bool(self.__protocol == 6)

    @property
    def isUDP(self):
        return bool(self.__protocol == 17)

    @property
    def SourceAddress(self):
        return self.__srcAddr

    @property
    def DestinationAddress(self):
        return self.__destAddr

    @property
    def payload(self):
        return self.__framebuffer[self.__HLEN * 4:self.__totalLength]

    def make_reply(self, payload, src=None):
        buf = [0x45, 0]
        totallength = 20 + len(payload)
        buf.extend([(totallength >> 8)&0xFF, totallength & 0xff])
        buf.extend(self.__framebuffer[4:6])
        buf.extend([0x40, 0])
        buf.extend(self.__framebuffer[8:10])
        buf.extend([0, 0])
        buf.extend(self.__framebuffer[16:20])
        buf.extend(self.__framebuffer[12:16])
        set_ip_checksum(buf)
        buf.extend(payload)
        return buf

    def __str__(self):
        if self.isICMP:
            return "ICMP"
        if self.isIGMP:
            return "IGMP"
        if self.isTCP:
            return "TCP"
        if self.isUDP:
            return "UDP"
