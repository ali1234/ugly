import numpy as np
import smbus
import time

from ugly.drivers.base import Driver
from ugly.drivers.hardware.i2c import Register, Command


class HT16K33(Driver):

    data = Register(0x00)

    config  = Command(0b00100000, 0b00000001)
    setup   = Command(0b10000000, 0b00000111)
    rowint  = Command(0b10100000, 0b00000011)
    dimming = Command(0b11100000, 0b00001111)

    def __init__(self, rawbuf, map, bus=1, address=0x70, name='HT16K33'):
        super().__init__(rawbuf, 1, name)
        self._bus = smbus.SMBus(bus)
        self._address = address

        self.__map = map

        self.config = 1
        time.sleep(0.001)
        self.setup = 1
        self.rowint = 0
        self.dimming = 0xf

    def show(self):
        bits = (self.gammabuf > 0x7f).flatten().take(self.__map, mode='clip')
        self.data = np.packbits(bits, axis=0).flatten().tolist()


class Homebrew(HT16K33):

    map = np.array([
        [  7,  -1,  22,  -1,  37,  -1,  52,  -1,  67,  -1,  82,  -1,  97,  -1,  -1,  -1],
        [  6,  14,  21,  29,  36,  44,  51,  59,  66,  74,  81,  89,  96, 104,  -1,  -1],
        [  5,  13,  20,  28,  35,  43,  50,  58,  65,  73,  80,  88,  95, 103,  -1,  -1],
        [  4,  12,  19,  27,  34,  42,  49,  57,  64,  72,  79,  87,  94, 102,  -1,  -1],
        [  3,  11,  18,  26,  33,  41,  48,  56,  63,  71,  78,  86,  93, 101,  -1,  -1],
        [  2,  10,  17,  25,  32,  40,  47,  55,  62,  70,  77,  85,  92, 100,  -1,  -1],
        [  1,   9,  16,  24,  31,  39,  46,  54,  61,  69,  76,  84,  91,  99,  -1,  -1],
        [  0,   8,  15,  23,  30,  38,  45,  53,  60,  68,  75,  83,  90,  98,  -1,  -1],
    ], dtype=np.int16)

    def __init__(self, bus=1, name='Homebrew'):
        super().__init__(np.zeros((7, 15, 1), dtype=np.uint8), self.map, bus=bus, name=name)
