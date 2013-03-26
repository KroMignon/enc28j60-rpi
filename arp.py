#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     arp.py
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

class ArpFrame(object):
    '''
    Arp Frame Decoder (cf. RFC792)

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |     Type      |     Code      |          Checksum             |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                             unused                            |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |      Internet Header + 64 bits of Original Data Datagram      |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    '''

    def __init__(self, framebuffer):
        '''
        Constructor
        '''
        self.__framebuffer = framebuffer
        self.__HAS = framebuffer[0] * 256 + framebuffer[1]
        self.__PAS = framebuffer[2] * 256 + framebuffer[3]
        self.__HALength = framebuffer[4]
        self.__PALength = framebuffer[5]
        self.__Command = framebuffer[6] * 256 + framebuffer[7]
        pos = 8
        self.__SHA = ":".join('%02x' % framebuffer[pos+idx] for idx in range(self.__HALength))
        pos += self.__HALength
        self.__SPA = ".".join('%d' % framebuffer[pos+idx] for idx in range(self.__PALength))
        pos += self.__PALength
        self.__THA = ":".join('%02x' % framebuffer[pos+idx] for idx in range(self.__HALength))
        pos += self.__HALength
        self.__TPA = ".".join('%d' % framebuffer[pos+idx] for idx in range(self.__PALength))
        pos += self.__PALength

    @property
    def isIP(self):
        return bool(self.__PAS == 0x0800)

    @property
    def isIPv4(self):
        return bool(self.__PAS == 0x0800 and self.__PALength == 4)

    @property
    def isIPv6(self):
        return bool(self.__PAS == 0x0800 and self.__PALength == 6)

    @property
    def HardwareAddressSpace(self):
        return self.__HAS

    @property
    def ProtocolAddressSpace(self):
        return self.__PAS

    @property
    def Command(self):
        return self.__Command

    @property
    def SenderHarwareAddress(self):
        return self.__SHA

    @property
    def SenderProtocolAddress(self):
        return self.__SPA

    @property
    def TargetHarwareAddress(self):
        return self.__THA

    @property
    def TargetProtocolAddress(self):
        return self.__TPA

    def make_reply(self, my_mac):

        buf = [self.__framebuffer[idx] for idx in range(8)]

        # Mise en place du code "Reply"
        buf[7] = 2

        # Mise en place de notre adresse MAC
        buf.extend([int(b, 16) for b in my_mac.split(':')])

        # Mise en place de notre adresse IP
        buf.extend([int(b) for b in self.TargetProtocolAddress.split('.')])

        # Mise en place de l'adresse MAC de la destination
        buf.extend([int(b, 16) for b in self.SenderHarwareAddress.split(':')])

        # Mise en place de l'adresse IP de la destination
        buf.extend([int(b) for b in self.SenderProtocolAddress.split('.')])

        return buf

