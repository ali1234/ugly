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

from ugly.drivers.base import Driver

from rpi_ws281x import PixelStrip

LED_COUNT      = 64      # Number of LED pixels.
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_GAMMA      = (((np.arange(0, 256) / 255) ** 2.25) * 255).astype(np.uint8).tolist()

class WS2812(Driver):
    """
    Legacy driver. Passes through calls to some other driver.
    """

    def __init__(self, width, height, led_pin=18, map=None, name=None):
        self.map = map
        if self.map is None:
            n_leds = self.height * self.width
        else:
            n_leds = len(self.map)
        super().__init__(np.zeros((height, width, 3), dtype=np.uint8), 8, name=name)
        self.pixelstrip = PixelStrip(n_leds, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_GAMMA)

    def __enter__(self):
        self.pixelstrip.begin()
        return super().__enter__()

    def show(self):
        if self.map is not None:
            outbuf = self.rawbuf[self.map]
        else:
            outbuf = self.rawbuf
        outbuf = outbuf.reshape(-1, 3)
        for i in range(outbuf.shape[0]):
            self.pixelstrip.setPixelColorRGB(i, *outbuf[i].tolist()) # ugh
        self.pixelstrip.show()
        super().show()
