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

import blinkt

class Blinkt(Driver, Drawable):
    """
    Legacy driver. Passes through calls to some other driver.
    """

    def __init__(self):
        super().__init__(np.zeros((1, 8, 3), dtype=np.uint8), 8, name='Blinkt')

    def __enter__(self):
        return super().__enter__()

    def show(self):
        blinkt.pixels = np.pad(self.rawbuf, ((0,0),(0,0),(0,1)), mode='constant', constant_values=blinkt.BRIGHTNESS)[0].tolist()
        blinkt.show()
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rawbuf[:] = 0
        self.show()
        super().__exit__(exc_type, exc_val, exc_tb)
