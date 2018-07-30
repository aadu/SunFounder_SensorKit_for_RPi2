#!/usr/bin/env python

import time

import smbus


class LCD1602:

    def __init__(self, address=0x27, backlight=1):
        self.address = address
        self.backlight = backlight
        self.bus = smbus.SMBus(1)
        self.initialize()

    def initialize(self):
        self.send_command(0x33)  # Must initialize to 8-line mode at first
        time.sleep(0.005)
        self.send_command(0x32)  # Then initialize to 4-line mode
        time.sleep(0.005)
        self.send_command(0x28)  # 2 Lines & 5*7 dots
        time.sleep(0.005)
        self.send_command(0x0C)  # Enable display without cursor
        time.sleep(0.005)
        self.send_command(0x01)  # Clear Screen
        self.bus.write_byte(self.address, 0x08)

    def write_word(self, data):
        if self.backlight == 1:
            data |= 0x08
        else:
            data &= 0xF7
        self.bus.write_byte(self.address, data)

    def send_command(self, comm):
        # Send bit7-4 firstly
        buf = comm & 0xF0
        buf |= 0x04  # RS = 0, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # Make EN = 0
        self.write_word(buf)

        # Send bit3-0 secondly
        buf = (comm & 0x0F) << 4
        buf |= 0x04  # RS = 0, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # Make EN = 0
        self.write_word(buf)

    def send_data(self, data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05  # RS = 1, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # Make EN = 0
        self.write_word(buf)

        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05  # RS = 1, RW = 0, EN = 1
        self.write_word(buf)
        time.sleep(0.002)
        buf &= 0xFB  # Make EN = 0
        self.write_word(buf)

    def clear(self):
        self.send_command(0x01)  # Clear Screen

    def openlight(self):  # Enable the backlight
        self.bus.write_byte(0x27, 0x08)
        self.bus.close()

    def write(self, x, y, txt):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y < 0:
            y = 0
        if y > 1:
            y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)
        for char in txt:
            self.send_data(ord(char))

