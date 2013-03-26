#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     Components.py
# Purpose:  Basic Command Line Interface for Orchestra elements
#
# Author:   Fabrice MOUSSET
#
# Created:  2008/01/17
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

__doc__ = "Classe de simulation du port SPI pour test sur PC"
__version__ = "1.0.0"
__versionTime__ = "xx/xx/xxxx"
__author__ = "Fabrice MOUSSET <fabrice.mousset@laposte.net>"

class SpiDev(object):
    mode = 0
    cshigh = False
    threewire = False
    lsbfirst = False
    loop = False
    bits_per_word = 8
    max_speed_hs = 50000
    def __init__(self):
        pass
    def open(self, bus=0, device=0):
        pass
    def close(self):
        pass
    def xfer2(self, data):
        pass