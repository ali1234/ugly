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

from ugly.buffer import Drawable
from ugly.drivers.base import Driver

from rpi_ws281x import PixelStrip

LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_GAMMA      = (((np.arange(0, 256) / 255) ** 2.25) * 255).astype(np.uint8).tolist()

class WS2812(Driver, Drawable):
    """
    Legacy driver. Passes through calls to some other driver.
    """

    def __init__(self, width, height, serpentine=False, name=None):
        self.serpentine = serpentine
        super().__init__(np.zeros((height, width, 3), dtype=np.uint8), 8, name=name)
        self.pixelstrip = PixelStrip(self.height*self.width, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_GAMMA)

    def __enter__(self):
        self.pixelstrip.begin()
        return super().__enter__()

    def show(self):
        if self.serpentine:
            # TODO: handle serpentine, but i don't have hardware to test :(
            outbuf = self.rawbuf
        else:
            outbuf = self.rawbuf
        outbuf = outbuf.reshape(self.width*self.height, 3)
        for i in range(outbuf.shape[0]):
            self.pixelstrip.setPixelColorRGB(i, *outbuf[i].tolist()) # ugh
        self.pixelstrip.show()
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rawbuf[:] = 0
        self.show()
        super().__exit__(exc_type, exc_val, exc_tb)
