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

import scrollphathd


class ScrollPhatHD(Driver):
    """
    Legacy driver. Passes through calls to some other driver.
    """

    def __init__(self):
        super().__init__(np.zeros((7, 17, 1), dtype=np.uint8), 8, name='ScrollPhatHD')

    def show(self):
        scrollphathd.display.buf = np.transpose(self.rawbuf[:,:,0] / 255, (1, 0))
        scrollphathd.show()
        super().show()
