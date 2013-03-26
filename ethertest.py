#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     ethertest.py
# Purpose:  Microchip ENC28J60 Ethernet Interface test
#
# Author:   Fabrice MOUSSET
#
# Created:  2013/01/13
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

"Microchip ENC28J60 Ethernet Interface test"
__version__ = "1.0.0"
__versionTime__ = "xx/xx/xxxx"
__author__ = "Fabrice MOUSSET <fabrice.mousset@laposte.net>"

from enc28j60 import Enc28j60
from ethernet import EthernetFrame
from arp import ArpFrame
from ip import IpFrame
from icmp import IcmpFrame
from udp import UdpFrame

import argparse
import logging

# Création du parseur de paramètres en ligne de commande
parser = argparse.ArgumentParser(description='Programme de test du ENC68J60')
parser.add_argument('-i', '--ip', default='192.168.2.55', help='Adresse IP local au format x.x.x.x')
parser.add_argument('-m', '--mac', default='00:90:3f:00:00:01', help='Adresse MAC local au format xx:xx:xx:xx:xx:xx')
parser.add_argument('-v', '--verbose', default=False, help='Pour afficher les message de debug')

# Gestion des message de debug
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)

args = parser.parse_args()
mac = [int(m,16) for m in args.mac.split(':')]
my_ip = args.ip

logger.info('Adresse MAC %s', ":".join('%02x' % m for m in mac))
logger.info('Adresse IP %s', my_ip)

enet = Enc28j60(0,0)
rev_id = enet.Initialize(mac)
logger.info('ENC28J60 Rev ID %d', rev_id)
linkup = enet.isLinkUp
while 1:
    if linkup != enet.isLinkUp:
        linkup = enet.isLinkUp
        logger.info("Link changed")
    buf = enet.PacketReceive()
    if buf:
        frame = EthernetFrame(buf)
        logger.info("Type is " + str(frame))
        logger.info("Eth source %s - Eth target %s" % (frame.srcMAC, frame.destMAC))

        if(frame.isARP):
            arp = ArpFrame(frame.payload)
            logger.info("ARP Command = %d" % arp.Command)
            if(arp.isIP):
                logger.info("ARP Source MAC %s" % arp.SenderHarwareAddress)
                logger.info("ARP Source IP %s" % arp.SenderProtocolAddress)
                logger.info("ARP Target MAC %s" % arp.TargetHarwareAddress)
                logger.info("ARP Target IP %s" % arp.TargetProtocolAddress)
                if(arp.TargetProtocolAddress == my_ip):
                    logger.info("My IP !!!!!")
                    my_reply = frame.make_reply(arp.make_reply(enet.MacAddress), enet.MacAddress)
                    logger.info("Request = %s" % " ".join('%02x' % b for b in buf))
                    logger.info("Reply   = %s" % " ".join('%02x' % b for b in my_reply))
                    enet.PacketSend(my_reply)

        if(frame.isIPv4):
            ipv4 = IpFrame(frame.payload)
            logger.info('Type is' + str(ipv4))
            if ipv4.isICMP:
                icmp = IcmpFrame(ipv4.payload)
                if(icmp.isEchoRequest):
                    logger.info("Send Echo reply")
                    logger.info("Request = %s" % " ".join('%02x' % b for b in buf))
                    my_reply = frame.make_reply(ipv4.make_reply(icmp.make_reply()), enet.MacAddress)
                    logger.info("Reply   = %s" % " ".join('%02x' % b for b in my_reply))
                    enet.PacketSend(my_reply)
