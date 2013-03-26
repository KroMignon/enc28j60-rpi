#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     udp.py
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

def make_udp_frame(src, dst, payload):
    buf = [(src >> 8) & 0xFF, src & 0xFF]
    buf.extend([(dst >> 8) & 0xff, dst & 0xff])
    size = len(payload)
    buf.extend([(size >> 8) & 0xff, size & 0xff])
    buf.extend([0, 0])
    buf.extend(payload)
    return buf

class UdpFrame(object):
    '''
    Classe de décodage des datagrammes UDP (cf. RFC768)

    User Datagram Header Format

         0      7 8     15 16    23 24    31
        +--------+--------+--------+--------+
        |     Source      |   Destination   |
        |      Port       |      Port       |
        +--------+--------+--------+--------+
        |                 |                 |
        |     Length      |    Checksum     |
        +--------+--------+--------+--------+
        |
        |          data octets ...
        |
        +---------------- ...

    '''

    def __init__(self, datagram):
        '''
        Constructor
        '''
        self.__datagram = datagram
        self.__srcPort = datagram[0] * 256 + datagram[1]
        self.__dstPort = datagram[2] * 256 + datagram[3]
        self.__size = datagram[4] * 256 + datagram[5]
        self.__csum = datagram[6] * 256 + datagram[7]

    @property
    def SourcePort(self):
        return self.__srcPort

    @property
    def DestinationPort(self):
        return self.__dstPort

    @property
    def CheckSum(self):
        return self.__csum

    @property
    def payload(self):
        return self.__datagram[8:self.__size]

    def make_reply(self, payload):
        return make_udp_frame(self.__dstPort, self.__srcPort, payload)
