#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     icmp.py
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

ICMP_REQUEST = {}

def set_icmp_checksum(buf):
    csum = 0
    # Clear previous Checksum value
    buf[2] = 0
    buf[3] = 0

    # Generate checksum
    for idx in range(len(buf)/2):
        val = buf[idx*2] * 256 + buf[idx*2+1]
        csum += val

    csum = ((csum >> 16) & 0xFFFF) + (csum & 0xFFFF)
    csum += (csum >> 16)
    csum = ~csum

    # Update checksum value in frame
    buf[2] = (csum >> 8) & 0xff
    buf[3] = csum  & 0xff

class IcmpFrame(object):
    '''
    Classe de decodage des trames ICMP - Internet Control Message Protocol
    '''
    def __init__(self, framebuffer):
        self.__type = framebuffer[0]
        self.__code = framebuffer[1]
        self.__checksum = framebuffer[2] * 256 + framebuffer[3]
        self.__id = framebuffer[4] * 256 + framebuffer[5]
        self.__seqNum = framebuffer[6] * 256 + framebuffer[7]

    @property
    def isEchoReply(self):
        return bool(self.__type == 0 and self.__code == 0)

    @property
    def isEchoRequest(self):
        return bool(self.__type == 8 and self.__code == 0)

    @property
    def Identification(self):
        return self.__id

    @property
    def SequenceNumber(self):
        return self.__seqNum

    def make_reply(self):
        if(self.isEchoRequest):
            buf = [0,0,0,0]
            buf.extend([(self.__id >> 8) & 0xff, self.__id & 0xff])
            buf.extend([(self.__seqNum >> 8) & 0xff, self.__seqNum & 0xff])
            set_icmp_checksum(buf)
            return buf
        return None
