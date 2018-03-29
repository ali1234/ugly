# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

import time
import numpy as np
import smbus

from ugly.drivers.base import Driver
from ugly.drivers.hardware.i2c import Register, BankedRegister

CONFIG_BANK = 0x0b
BANK_REGISTER = 0xfd

PICTURE_MODE = 0x00
AUTOPLAY_MODE = 0x08
AUDIOPLAY_MODE = 0x18


class IS31FL3731(Driver):

    bank = Register(BANK_REGISTER)

    mode = BankedRegister(BANK_REGISTER, CONFIG_BANK, 0x00)
    frame = BankedRegister(BANK_REGISTER, CONFIG_BANK, 0x01)
    audiosync = BankedRegister(BANK_REGISTER, CONFIG_BANK, 0x06)
    shutdown = BankedRegister(BANK_REGISTER, CONFIG_BANK, 0x0a)

    enable = Register(0x00)
    blink = Register(0x12)
    pwm = Register(0x24)

    def __init__(self, rawbuf, map, bus=1, address=0x74, name='IS31FL3731'):
        super().__init__(rawbuf, 8, name)
        self._bus = smbus.SMBus(bus)
        self._address = address
        self.__current_frame = 0
        self.__map = map

        self.reset()

        self.mode = PICTURE_MODE
        self.audiosync = 0
        self.frame = self.__current_frame

        enable_pattern = np.packbits(self.__map.reshape(-1, 8)[:,::-1] >= 0)

        for bank in range(8):
            self.bank = bank
            self.enable = enable_pattern.tolist()

    def show(self):
        self.__current_frame += 1
        self.__current_frame %= 8 # use all the banks...

        self.bank = self.__current_frame
        self.pwm = self.gammabuf.flatten().take(self.__map, mode='clip').tolist()
        self.frame = self.__current_frame
        super().show()

    def reset(self):
        self.sleep(True)
        time.sleep(0.00001)
        self.sleep(False)

    def sleep(self, value):
        self.shutdown = not value


class ScrollPhatHD(IS31FL3731):

    map = np.array([
        110,  93,  76,  59,  42,  25,   8,  -1,   9,  26,  43,  60,  77,  94, 111,  -1,
        109,  92,  75,  58,  41,  24,   7,  -1,  10,  27,  44,  61,  78,  95, 112,  -1,
        108,  91,  74,  57,  40,  23,   6,  -1,  11,  28,  45,  62,  79,  96, 113,  -1,
        107,  90,  73,  56,  39,  22,   5,  -1,  12,  29,  46,  63,  80,  97, 114,  -1,
        106,  89,  72,  55,  38,  21,   4,  -1,  13,  30,  47,  64,  81,  98, 115,  -1,
        105,  88,  71,  54,  37,  20,   3,  -1,  14,  31,  48,  65,  82,  99, 116,  -1,
        104,  87,  70,  53,  36,  19,   2,  -1,  15,  32,  49,  66,  83, 100, 117,  -1,
        103,  86,  69,  52,  35,  18,   1,  -1,  16,  33,  50,  67,  84, 101, 118,  -1,
        102,  85,  68,  51,  34,  17,   0,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,
    ], dtype=np.int16)

    def __init__(self, bus=1, name='ScrollPhatHD'):
        super().__init__(np.zeros((7, 17, 1), dtype=np.uint8), self.map, bus=bus, name=name)
