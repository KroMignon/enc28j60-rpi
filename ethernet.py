#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     ethernet.py
# Purpose:  Microchip ENC28J60 Ethernet Interface Driver
#
# Author:   Fabrice MOUSSET
#
# Created:  2013/01/05
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

class EthernetFrame(object):
    def __init__(self, framebuffer):
        self.__framebuffer = framebuffer
        self.__destMAC = ":".join('%02x' % i for i in self.__framebuffer[0:6])
        self.__srcMAC = ":".join('%02x' % i for i in self.__framebuffer[6:12])
        self.__frameType = self.__framebuffer[12] * 256 + self.__framebuffer[13]

    @property
    def destMAC(self):
        return self.__destMAC

    @property
    def srcMAC(self):
        return self.__srcMAC

    @property
    def frameType(self):
        return  self.__frameType

    @property
    def isARP(self):
        return bool(self.__frameType == 0x0806)

    @property
    def isIPv4(self):
        return bool(self.__frameType == 0x0800)

    @property
    def isIPv6(self):
        return bool(self.__frameType == 0x08DD)

    @property
    def payload(self):
        return self.__framebuffer[14:]

    def __str__(self):
        if self.isARP:
            return "ARP"
        if self.isIPv4:
            return "IPv4"
        if self.isIPv6:
            return "IPv6"
        return "Unknown"

    def make_header(self, buf, dst_mac=None):
        pass

    def make_reply(self, payload, mac=None):
        buf = [self.__framebuffer[6+b] for b in range(6)]
        if(mac):
            buf.extend([int(m,16) for m in mac.split(':')])
        else:
            buf.extend(self.__framebuffer[0:6])
        buf.extend(self.__framebuffer[12:14])
        buf.extend(payload)
        return buf
