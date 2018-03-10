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

import scrollphat


class ScrollPhat(Driver, Drawable):
    """
    Legacy driver. Passes through calls to some other driver.
    Does not need its own framebuffer as the legacy driver has one.
    """
    # TODO: may need multiple versions of this
    # as the legacy drivers are all slightly different.

    def __init__(self):
        super().__init__(np.zeros((5, 11, 1), dtype=np.uint8), 1, name='ScrollPhat')

    def __enter__(self):
        return super().__enter__()

    def show(self):
        packed = np.packbits(np.pad( (self.rawbuf[::-1,:,0] & 0x80) > 0, ((3,0),(0,0)), mode='constant'), axis=0)
        scrollphat.set_buffer(packed[0].tolist())
        scrollphat.update()
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        scrollphat.clear()
        super().__exit__(exc_type, exc_val, exc_tb)
