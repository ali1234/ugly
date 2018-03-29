# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

import numpy as np
import smbus

from ugly.drivers.base import Driver
from ugly.drivers.hardware.i2c import Register


class IS31FL3730(Driver):

    mode = Register(0x00)
    data1 = Register(0x01)
    data2 = Register(0x0e)
    update = Register(0x0c)
    brightness = Register(0x19)
    reset = Register(0xff)

    def __init__(self, rawbuf, map1=None, map2=None, bus=1, address=0x60, name='IS31FL3730'):
        super().__init__(rawbuf, 1, name)
        self._bus = smbus.SMBus(bus)
        self._address = address

        if map1 is None and map2 is None:
            raise Exception('Need at least one map.')

        mode = 0

        if map2 is not None:
            mode |= 0b00001000
            if map1 is not None:
                if map1.shape != map2.shape:
                    raise Exception('Maps must be the same shape.')
                else:
                    mode |= 0b00010000

        shape = map2.shape if map1 is None else map1.shape
        if shape[0] == 8 and shape[1] >= 8 and shape[1] <= 11:
            mode |= shape[1] - 8
        else:
            raise Exception('Map shape not valid for display.')

        self.__map1 = map1
        self.__map2 = map2

        self.reset = 0
        self.mode = mode

    def show(self):
        if self.__map1 is not None:
            bits = (self.gammabuf > 0x7f).flatten().take(self.__map1, mode='clip')
            self.data1 = np.packbits(bits, axis=0).flatten().tolist()

        if self.__map2 is not None:
            bits = (self.gammabuf > 0x7f).flatten().take(self.__map2, mode='clip')
            self.data2 = np.packbits(bits, axis=0).flatten().tolist()

        self.update = 0
        super().show()


class ScrollPhat(IS31FL3730):

    map1 = np.array([
        [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1],
        [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1],
        [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1],
        [ 44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54],
        [ 33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  43],
        [ 22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32],
        [ 11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21],
        [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10],
    ], dtype=np.int16)

    def __init__(self, bus=1, name='ScrollPhat'):
        super().__init__(np.zeros((5, 11, 1), dtype=np.uint8), map1=self.map1, map2=None, bus=bus, name=name)
