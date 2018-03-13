import numpy as np
import smbus

from ugly.drivers.base import Driver
from ugly.drivers.hardware.i2c import Register


class IS31FL3730(Driver):

    mode = Register(0x00)
    data = Register(0x01)
    brightness = Register(0x19)

    def __init__(self, rawbuf, bus=1, address=0x60, name='IS31FL3730'):
        super().__init__(rawbuf, 1, name)
        self._bus = smbus.SMBus(bus)
        self._address = address

        self.mode = 0b00000011

    def show(self):
        bits = np.pad(self.gammabuf > 0x7f, ((0,3), (0,0), (0,0)), mode='constant')[::-1]
        outbuf = np.packbits(bits, axis=0).flatten().tolist()
        outbuf.append(0xff)
        self.data = outbuf


class ScrollPhat(IS31FL3730):

    def __init__(self, bus=1, name='ScrollPhat'):
        super().__init__(np.zeros((5, 11, 1), dtype=np.uint8), bus=bus, name=name)
