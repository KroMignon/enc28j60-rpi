#! /usr/bin/python
# -*- coding: utf-8 -*-
#=============================================================================
# Name:     enc28j60.py
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

"Microchip ENC28J60 Ethernet Interface Driver"
__version__ = "1.0.0"
__versionTime__ = "xx/xx/xxxx"
__author__ = "Fabrice MOUSSET <fabrice.mousset@laposte.net>"

import spidev

ADDR_MASK = 0x1F
BANK_MASK = 0x60
SPRD_MASK = 0x80

# All-bank registers
EIE   = 0x1B
EIR   = 0x1C
ESTAT = 0x1D
ECON2 = 0x1E
ECON1 = 0x1F

# Bank 0 registers
ERDPT   = (0x00|0x00)
EWRPT   = (0x02|0x00)
ETXST   = (0x04|0x00)
ETXND   = (0x06|0x00)
ERXST   = (0x08|0x00)
ERXND   = (0x0A|0x00)
ERXRDPT = (0x0C|0x00)
ERXWRPT = (0x0E|0x00)
EDMAST  = (0x10|0x00)
EDMAND  = (0x12|0x00)
EDMADST = (0x14|0x00)
EDMACS  = (0x16|0x00)
# Bank 1 registers
EHT0    = (0x00|0x20)
EHT1    = (0x01|0x20)
EHT2    = (0x02|0x20)
EHT3    = (0x03|0x20)
EHT4    = (0x04|0x20)
EHT5    = (0x05|0x20)
EHT6    = (0x06|0x20)
EHT7    = (0x07|0x20)
EPMM0   = (0x08|0x20)
EPMM1   = (0x09|0x20)
EPMM2   = (0x0A|0x20)
EPMM3   = (0x0B|0x20)
EPMM4   = (0x0C|0x20)
EPMM5   = (0x0D|0x20)
EPMM6   = (0x0E|0x20)
EPMM7   = (0x0F|0x20)
EPMCS   = (0x10|0x20)
EPMO    = (0x14|0x20)
EWOLIE  = (0x16|0x20)
EWOLIR  = (0x17|0x20)
ERXFCON = (0x18|0x20)
EPKTCNT = (0x19|0x20)
# Bank 2 registers
MACON1   = (0x00|0x40|0x80)
MACON2   = (0x01|0x40|0x80)
MACON3   = (0x02|0x40|0x80)
MACON4   = (0x03|0x40|0x80)
MABBIPG  = (0x04|0x40|0x80)
MAIPG    = (0x06|0x40|0x80)
MACLCON1 = (0x08|0x40|0x80)
MACLCON2 = (0x09|0x40|0x80)
MAMXFL   = (0x0A|0x40|0x80)
MAPHSUP  = (0x0D|0x40|0x80)
MICON    = (0x11|0x40|0x80)
MICMD    = (0x12|0x40|0x80)
MIREGADR = (0x14|0x40|0x80)
MIWRL    = (0x16|0x40|0x80)
MIWRH    = (0x17|0x40|0x80)
MIRDL    = (0x18|0x40|0x80)
MIRDH    = (0x19|0x40|0x80)
# Bank 3 registers
MAADR1  = (0x00|0x60|0x80)
MAADR0  = (0x01|0x60|0x80)
MAADR3  = (0x02|0x60|0x80)
MAADR2  = (0x03|0x60|0x80)
MAADR5  = (0x04|0x60|0x80)
MAADR4  = (0x05|0x60|0x80)
EBSTSD  = (0x06|0x60)
EBSTCON = (0x07|0x60)
EBSTCS  = (0x08|0x60)
MISTAT  = (0x0A|0x60|0x80)
EREVID  = (0x12|0x60)
ECOCON  = (0x15|0x60)
EFLOCON = (0x17|0x60)
EPAUS   = (0x18|0x60)

# ENC28J60 ERXFCON Register Bit Definitions
ERXFCON_UCEN  = 0x80
ERXFCON_ANDOR = 0x40
ERXFCON_CRCEN = 0x20
ERXFCON_PMEN  = 0x10
ERXFCON_MPEN  = 0x08
ERXFCON_HTEN  = 0x04
ERXFCON_MCEN  = 0x02
ERXFCON_BCEN  = 0x01
# ENC28J60 EIE Register Bit Definitions
EIE_INTIE  = 0x80
EIE_PKTIE  = 0x40
EIE_DMAIE  = 0x20
EIE_LINKIE = 0x10
EIE_TXIE   = 0x08
EIE_WOLIE  = 0x04
EIE_TXERIE = 0x02
EIE_RXERIE = 0x01
# ENC28J60 EIR Register Bit Definitions
EIR_PKTIF  = 0x40
EIR_DMAIF  = 0x20
EIR_LINKIF = 0x10
EIR_TXIF   = 0x08
EIR_WOLIF  = 0x04
EIR_TXERIF = 0x02
EIR_RXERIF = 0x01
# ENC28J60 ESTAT Register Bit Definitions
ESTAT_INT     = 0x80
ESTAT_LATECOL = 0x10
ESTAT_RXBUSY  = 0x04
ESTAT_TXABRT  = 0x02
ESTAT_CLKRDY  = 0x01
# ENC28J60 ECON2 Register Bit Definitions
ECON2_AUTOINC = 0x80
ECON2_PKTDEC  = 0x40
ECON2_PWRSV   = 0x20
ECON2_VRPS    = 0x08
# ENC28J60 ECON1 Register Bit Definitions
ECON1_TXRST  = 0x80
ECON1_RXRST  = 0x40
ECON1_DMAST  = 0x20
ECON1_CSUMEN = 0x10
ECON1_TXRTS  = 0x08
ECON1_RXEN   = 0x04
ECON1_BSEL1  = 0x02
ECON1_BSEL0  = 0x01
# ENC28J60 MACON1 Register Bit Definitions
MACON1_LOOPBK  = 0x10
MACON1_TXPAUS  = 0x08
MACON1_RXPAUS  = 0x04
MACON1_PASSALL = 0x02
MACON1_MARXEN  = 0x01
# ENC28J60 MACON2 Register Bit Definitions
MACON2_MARST   = 0x80
MACON2_RNDRST  = 0x40
MACON2_MARXRST = 0x08
MACON2_RFUNRST = 0x04
MACON2_MATXRST = 0x02
MACON2_TFUNRST = 0x01
# ENC28J60 MACON3 Register Bit Definitions
MACON3_PADCFG2 = 0x80
MACON3_PADCFG1 = 0x40
MACON3_PADCFG0 = 0x20
MACON3_TXCRCEN = 0x10
MACON3_PHDRLEN = 0x08
MACON3_HFRMLEN = 0x04
MACON3_FRMLNEN = 0x02
MACON3_FULDPX  = 0x01
# ENC28J60 MICMD Register Bit Definitions
MICMD_MIISCAN = 0x02
MICMD_MIIRD   = 0x01
# ENC28J60 MISTAT Register Bit Definitions
MISTAT_NVALID = 0x04
MISTAT_SCAN   = 0x02
MISTAT_BUSY   = 0x01

# PHY registers
PHCON1  = 0x00
PHSTAT1 = 0x01
PHHID1  = 0x02
PHHID2  = 0x03
PHCON2  = 0x10
PHSTAT2 = 0x11
PHIE    = 0x12
PHIR    = 0x13
PHLCON  = 0x14

# ENC28J60 PHY PHCON1 Register Bit Definitions
PHCON1_PRST    = 0x8000
PHCON1_PLOOPBK = 0x4000
PHCON1_PPWRSV  = 0x0800
PHCON1_PDPXMD  = 0x0100
# ENC28J60 PHY PHSTAT1 Register Bit Definitions
PHSTAT1_PFDPX  = 0x1000
PHSTAT1_PHDPX  = 0x0800
PHSTAT1_LLSTAT = 0x0004
PHSTAT1_JBSTAT = 0x0002
# ENC28J60 PHY PHCON2 Register Bit Definitions
PHCON2_FRCLINK = 0x4000
PHCON2_TXDIS   = 0x2000
PHCON2_JABBER  = 0x0400
PHCON2_HDLDIS  = 0x0100

# ENC28J60 Packet Control Byte Bit Definitions
PKTCTRL_PHUGEEN   = 0x08
PKTCTRL_PPADEN    = 0x04
PKTCTRL_PCRCEN    = 0x02
PKTCTRL_POVERRIDE = 0x01

# SPI Operation Codes
ENC28J60_READ_CTRL_REG  = 0x00
ENC28J60_READ_BUF_MEM   = 0x3A
ENC28J60_WRITE_CTRL_REG = 0x40
ENC28J60_WRITE_BUF_MEM  = 0x7A
ENC28J60_BIT_FIELD_SET  = 0x80
ENC28J60_BIT_FIELD_CLR  = 0xA0
ENC28J60_SOFT_RESET     = 0xFF

# The RXSTART_INIT must be zero. See Rev. B4 Silicon Errata point 5.
# Buffer boundaries applied to internal 8K ram
# the entire available packet buffer space is allocated

RXSTART_INIT       = 0x0000  # start of RX buffer, room for 2 packets
RXSTOP_INIT        = 0x0BFF  # end of RX buffer

TXSTART_INIT       = 0x0C00  # start of TX buffer, room for 1 packet
TXSTOP_INIT        = 0x11FF  # end of TX buffer

SCRATCH_START      = 0x1200  # start of scratch area
SCRATCH_LIMIT      = 0x2000  # past end of area, i.e. 3.5 Kb
SCRATCH_PAGE_SHIFT = 6       # addressing is in pages of 64 bytes
SCRATCH_PAGE_SIZE  = (1 << SCRATCH_PAGE_SHIFT)

# max frame length which the controller will accept:
# (note: maximum Ethernet frame length would be 1518)
MAX_FRAMELEN       = 1500

class PacketHeader(object):
    HEADER_SIZE = 6
    __nextPacket = 0
    __byteCount = 0
    __status = 0
    __buf = []

    def __init__(self, buf):
        self.__buf = buf
        self.__nextPacket = buf[1] * 256 + buf[0]
        self.__byteCount = buf[3] * 256 + buf[2]
        self.__status = buf[5] * 256 + buf[4]
    @property
    def byteCount(self):
        """
        Indicates length of the received frame. This includes the destination
address, source address, type/length, data, padding and CRC fields.
        """
        return self.__byteCount;

    @property
    def nextPacket(self):
        """
        Next Packet Pointer.
        """
        return self.__nextPacket;

    @property
    def dropEvent(self):
        """
        Indicates a packet over 50,000 bit times occurred or that a packet was
        dropped since the last receive.
        """
        return bool(self.__status & 0x0001)

    @property
    def carrierEvent(self):
        """
        Indicates that at some time since the last receive, a carrier event was
detected. The carrier event is not associated with this packet. A carrier
event is activity on the receive channel that does not result in a packet
receive attempt being made.
        """
        return bool((self.__status >> 2) & 0x0001)

    @property
    def errorCRC(self):
        """
        Indicates that frame CRC field value does not match the CRC calculated
by the MAC.
        """
        return bool((self.__status >> 4) & 0x0001)

    @property
    def errorLengthCheck(self):
        """
        Indicates that frame length field value in the packet does not match the
actual data byte length and specifies a valid length.
        """
        return bool((self.__status >> 5) & 0x0001)

    @property
    def errorLengthOutOfRange(self):
        """
        Indicates that frame type/length field was larger than 1500 bytes (type field).
        """
        return bool((self.__status >> 6) & 0x0001)

    @property
    def receiveOk(self):
        """
        Indicates that at the packet had a valid CRC and no symbol errors.
        """
        return bool((self.__status >> 7) & 0x0001)

    @property
    def receiveMulticastPacket(self):
        """
        Indicates packet received had a valid Multicast address.
        """
        return bool((self.__status >> 8) & 0x0001)

    @property
    def receiveBroadcastPacket(self):
        """
        Indicates packet received had a valid Broadcast address.
        """
        return bool((self.__status >> 9) & 0x0001)

    @property
    def dribbleNible(self):
        """
        Indicates that after the end of this packet, an additional 1 to 7 bits were
received. The extra bits were thrown away.
        """
        return bool((self.__status >> 10) & 0x0001)

    @property
    def receiveControlFrame(self):
        """
        Current frame was recognized as a control frame for having a valid
type/length designating it as a control frame.
        """
        return bool((self.__status >> 11) & 0x0001)

    @property
    def receivePauseControlFrame(self):
        """
        Current frame was recognized as a control frame containing a valid pause
frame opcode and a valid destination address.
        """
        return bool((self.__status >> 12) & 0x0001)

    @property
    def receiveUnknownOpCode(self):
        """
        Current frame was recognized as a control frame but it contained an
unknown opcode.
        """
        return bool((self.__status >> 13) & 0x0001)

    @property
    def receiveVLANTypeDetected(self):
        """
        Current frame was recognized as a VLAN tagged frame.
        """
        return bool((self.__status >> 14) & 0x0001)

    def payload(self):
        """
        Header data
        """
        return self.__buf

class Enc28j60(object):
    __spi = None
    __Enc28j60Bank = -1
    __gNextPacketPtr = 0
    __MAC =  ""

    def __init__(self, bus=0, device=0):
        self.__spi = spidev.SpiDev()
        self.__spi.open(bus,device)
        # SPI_CPOL : 1 = Idle High
        # SPI_CPHA : 1 = Sample on falling edge
        #self.__spi.mode = (SPI_CPOL * 2) | SPI_CPHA

        # CS active low
        self.__spi.cshigh = False
        # MISO/MOSI not shared
        self.__spi.threewire = False
        self.__spi.lsbfirst = False
        self.__spi.loop = False
        self.__spi.bits_per_word = 8
        self.__spi.max_speed_hz = 2000000

    def Reset(self):
        pass

    def __readOp(self, opCode, addr):
        data = [(opCode | (addr & ADDR_MASK)), 0x00]
        # Pour les registres MAC et MII, il faut lire 1 octet en plus
        if(addr & 0x80):
            data.append(0x00)

        value = self.__spi.xfer2(data)
        return value[-1]

    def __writeOp(self, opCode, addr, data):
        return self.__spi.xfer2([(opCode | (addr & ADDR_MASK)), data])

    def __readBuffer(self, size):
        buf = size * [0]
        buf.insert(0, ENC28J60_READ_BUF_MEM)
        data = self.__spi.xfer2(buf)
        return data[1:]

    def __writeBuffer(self, buf):
        data = list(buf)
        data.insert(0, ENC28J60_WRITE_BUF_MEM)
        self.__spi.xfer2(data)

    def __setBank(self, bank):
        if((bank & BANK_MASK) != self.__Enc28j60Bank):
            self.__Enc28j60Bank = (bank & BANK_MASK)
            self.__writeOp(ENC28J60_BIT_FIELD_CLR, ECON1, ECON1_BSEL1|ECON1_BSEL0)
            self.__writeOp(ENC28J60_BIT_FIELD_SET, ECON1, self.__Enc28j60Bank>>5)

    def __readRegByte(self, addr):
        self.__setBank(addr)
        return self.__readOp(ENC28J60_READ_CTRL_REG, addr)

    def __writeRegByte(self, addr, value):
        self.__setBank(addr)
        self.__writeOp(ENC28J60_WRITE_CTRL_REG, addr, value)

    def __writeReg(self, addr, value):
        self.__writeRegByte(addr, value & 0xFF)
        self.__writeRegByte(addr+1, (value>>8) & 0xFF)

    def __readPhy(self, addr):
        self.__writeRegByte(MIREGADR, addr)
        self.__writeRegByte(MICMD, MICMD_MIIRD)
        while(self.__readRegByte(MISTAT) & MISTAT_BUSY):
            pass
        self.__writeRegByte(MICMD, 0x00)
        return self.__readRegByte(MIRDH) * 256 + self.__readRegByte(MIRDL)

    def __writePhy(self, addr, value):
        self.__writeRegByte(MIREGADR, addr)
        self.__writeReg(MIWRL, value)
        self.__writeReg(MIWRH, (value>>8)&0xff)
        while(self.__readRegByte(MISTAT) & MISTAT_BUSY):
            pass

    @property
    def MacAddress(self):
        return self.__MAC

    def Initialize(self, macaddress):
        self.__writeOp(ENC28J60_SOFT_RESET, 0, ENC28J60_SOFT_RESET)
        while((self.__readRegByte(ESTAT) & ESTAT_CLKRDY) == 0):
            pass

        self.__MAC = ":".join('%02x' % mac for mac in macaddress)

        # Initialize receive buffer
        self.__gNextPacketPtr = RXSTART_INIT;
        # Set receive buffer start address
        self.__writeReg(ERXST, RXSTART_INIT);
        # Set receive pointer address
        self.__writeReg(ERXRDPT, RXSTART_INIT);
        # Rx End
        self.__writeReg(ERXND, RXSTOP_INIT);
        # Tx Start
        self.__writeReg(ETXST, TXSTART_INIT);
        # Tx End
        self.__writeReg(ETXND, TXSTOP_INIT);


        # Do bank 1 stuff, packet filter:
        # For broadcast packets we allow only ARP packtets
        # All other packets should be unicast only for our mac (MAADR)
        #
        # The pattern to match on is therefore
        # Type     ETH.DST
        # ARP      BROADCAST
        # 06 08 -- ff ff ff ff ff ff -> ip checksum for theses bytes=f7f9
        # In binary these positions are:11 0000 0011 1111
        # This is hex 303F
        self.__writeRegByte(ERXFCON, ERXFCON_UCEN|ERXFCON_CRCEN|ERXFCON_PMEN);
        self.__writeReg(EPMM0, 0x303f);
        self.__writeReg(EPMCS, 0xf7f9);

        # Enable MAC receive
        self.__writeRegByte(MACON1, MACON1_MARXEN|MACON1_TXPAUS|MACON1_RXPAUS);
        # Bring MAC out of reset
        self.__writeRegByte(MACON2, 0x00);
        # Enable automatic padding to 60bytes and CRC operations
        self.__writeOp(ENC28J60_BIT_FIELD_SET, MACON3,
                            MACON3_PADCFG0|MACON3_TXCRCEN|MACON3_FRMLNEN);
        # Set inter-frame gap (non-back-to-back)
        self.__writeReg(MAIPG, 0x0C12);
        # Set inter-frame gap (back-to-back)
        self.__writeRegByte(MABBIPG, 0x12);
        # Set the maximum packet size which the controller will accept
        # Do not send packets longer than MAX_FRAMELEN:
        self.__writeReg(MAMXFL, MAX_FRAMELEN);

        # Write MAC address
        # NOTE: MAC address in ENC28J60 is byte-backward
        self.__writeRegByte(MAADR5, macaddress[0]);
        self.__writeRegByte(MAADR4, macaddress[1]);
        self.__writeRegByte(MAADR3, macaddress[2]);
        self.__writeRegByte(MAADR2, macaddress[3]);
        self.__writeRegByte(MAADR1, macaddress[4]);
        self.__writeRegByte(MAADR0, macaddress[5]);

        # No loopback of transmitted frames
        self.__writePhy(PHCON2, PHCON2_HDLDIS);

        # Switch to bank 0
        self.__setBank(ECON1);
        # Enable interrutps
        self.__writeOp(ENC28J60_BIT_FIELD_SET, EIE, EIE_INTIE|EIE_PKTIE);
        # Enable packet reception
        self.__writeOp(ENC28J60_BIT_FIELD_SET, ECON1, ECON1_RXEN);

        return self.__readRegByte(EREVID);

    @property
    def isLinkUp(self):
        return bool((self.__readPhy(PHSTAT2) >> 10) & 1)

    def PacketSend(self, buf):
        while (self.__readRegByte(ECON1) & ECON1_TXRTS):
            if (self.__readRegByte(EIR) & EIR_TXERIF):
                self.__writeOp(ENC28J60_BIT_FIELD_SET, ECON1, ECON1_TXRST)
                self.__writeOp(ENC28J60_BIT_FIELD_CLR, ECON1, ECON1_TXRST)

        # Set the write pointer to start of transmit buffer area
        self.__writeReg(EWRPT, TXSTART_INIT)
        # Set the TXND pointer to correspond to the packet size given
        self.__writeReg(ETXND, TXSTART_INIT+len(buf))
        # Write per-packet control byte (0x00 means use macon3 settings)
        self.__writeOp(ENC28J60_WRITE_BUF_MEM, 0, 0x00)
        # Copy the packet into the transmit buffer
        self.__writeBuffer(buf)
        # Send the contents of the transmit buffer onto the network
        self.__writeOp(ENC28J60_BIT_FIELD_SET, ECON1, ECON1_TXRTS)
        # Reset the transmit logic problem. See Rev. B4 Silicon Errata point 12.
        if (self.__readRegByte(EIR) & EIR_TXERIF):
            self.__writeOp(ENC28J60_BIT_FIELD_CLR, ECON1, ECON1_TXRST)

    def PacketReceive(self):
        buf = []
        if(self.__readRegByte(EPKTCNT) > 0):
            #print "packet detected"
            self.__writeReg(ERDPT, self.__gNextPacketPtr)
            header = PacketHeader(self.__readBuffer(PacketHeader.HEADER_SIZE))

            if header.byteCount > 1024:
                #print "Paquet size = %d" % header.byteCount
                #print header.payload()
                pass

            self.__gNextPacketPtr = header.nextPacket
            length = header.byteCount - 4 # Remove CRC from count
            if(header.receiveOk):
                buf = self.__readBuffer(length)
            if (self.__gNextPacketPtr - 1 > RXSTOP_INIT):
                self.__writeReg(ERXRDPT, RXSTOP_INIT)
            else:
                self.__writeReg(ERXRDPT, self.__gNextPacketPtr - 1)
            self.__writeOp(ENC28J60_BIT_FIELD_SET, ECON2, ECON2_PKTDEC)

        return buf

    def Leds(self, status=-1):
        if(status<0):
            self.__writePhy(PHLCON, 0x476)
        else:
            led_cfg = 0x990
            if((status & 1) == 1):
                led_cfg &= ~0x010
            if((status & 2) == 2):
                led_cfg &= ~0x100
            self.__writePhy(PHLCON, led_cfg)
        
if __name__ == "__main__":
    from time import sleep

    enet = Enc28j60(0,0)
    print enet.Initialize([0x00, 0x90, 0x3F, 0x00, 0x00, 0x01])
    enet.Leds(0)
    sleep(0.5)
    enet.Leds(1)
    sleep(0.5)
    enet.Leds(2)
    sleep(0.5)
    enet.Leds(3)
    sleep(0.5)
    enet.Leds(-1)
