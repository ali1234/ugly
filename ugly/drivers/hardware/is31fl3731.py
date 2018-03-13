import time
import numpy as np
import smbus

from ugly.buffer import Drawable
from ugly.drivers.base import Driver

CONFIG_BANK = 0x0b
BANK_ADDRESS = 0xfd

PICTURE_MODE = 0x00
AUTOPLAY_MODE = 0x08
AUDIOPLAY_MODE = 0x18


class Register(object):

    def __init__(self, offset):
        self.__offset = offset

    def __get__(self, obj, objtype):
        return obj.i2c.readfrom_mem(obj.address, self.__offset, 1)[0]

    def __set__(self, obj, value):
        if type(value) is list:
            for i in range(0, len(value), 32):
                obj.i2c.write_i2c_block_data(obj.address, self.__offset+i, value[i:i+32])
        else:
            obj.i2c.write_i2c_block_data(obj.address, self.__offset, [value])


class BankedRegister(Register):

    def __init__(self, bank, offset):
        super().__init__(offset)
        self.__bank = bank

    def __get__(self, obj, objtype):
        obj.i2c.write_i2c_block_data(obj.address, BANK_ADDRESS, [self.__bank])
        return super().__get__(obj, objtype)

    def __set__(self, obj, value):
        obj.i2c.write_i2c_block_data(obj.address, BANK_ADDRESS, [self.__bank])
        return super().__set__(obj, value)


class IS31FL3731(Driver, Drawable):

    bank = Register(BANK_ADDRESS)
    mode = BankedRegister(CONFIG_BANK, 0x00)
    frame = BankedRegister(CONFIG_BANK, 0x01)
    audiosync = BankedRegister(CONFIG_BANK, 0x06)
    shutdown = BankedRegister(CONFIG_BANK, 0x0a)

    enable = Register(0x00)
    blink = Register(0x12)
    pwm = Register(0x24)

    def __init__(self, rawbuf, depth, map, i2c=1, address=0x74, name='IS31FL3731'):
        super().__init__(rawbuf, depth, name)
        self.__i2c = smbus.SMBus(i2c)
        self.__address = address
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

    @property
    def i2c(self):
        return self.__i2c

    @property
    def address(self):
        return self.__address

    def show(self):
        self.__current_frame += 1
        self.__current_frame %= 8 # use all the banks...
        self.bank = self.__current_frame
        self.pwm = self.gammabuf.flatten().take(self.__map, mode='clip').tolist()
        self.frame = self.__current_frame

    def reset(self):
        self.sleep(True)
        time.sleep(0.00001)
        self.sleep(False)

    def sleep(self, value):
        self.shutdown = not value

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rawbuf[:] = 0
        self.show()
        super().__exit__(exc_type, exc_val, exc_tb)


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

    def __init__(self, i2c=1, name='ScrollPhatHD'):
        super().__init__(np.zeros((7, 17, 1), dtype=np.uint8), 8, self.map, i2c=i2c, name=name)

