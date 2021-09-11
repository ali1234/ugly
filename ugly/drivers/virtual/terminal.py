# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.


import sys

import numpy as np

from ugly.drivers.base import Driver, Virtual


class TerminalMonitor(Virtual):
    """
    Emulates a graphics device on the terminal.
    """

    def __init__(self, *args, mask=None, **kwargs):
        super().__init__(*args, **kwargs)
        if mask is not None:
            self.charmask = (mask * (0x25cf-ord(' '))) + ord(' ')
        else:
            self.charmask = np.full_like(self.rawbuf, 0x25cf)

    def __enter__(self):
        sys.stdout.write('\033[2J\033[?25l')
        return super().__enter__()

    def show(self):
        r = 0
        g = 1%self.channels
        b = 2%self.channels

        outbuf = self.convert_buffer()

        for y, row in enumerate(outbuf):
            sys.stdout.write('\033[{};0H'.format(y+2))
            sys.stdout.write('   ')
            s = ' '.join(
                ('\033[38;2;{:d};{:d};{:d}m{:c}'.format(pixel[r], pixel[g], pixel[b], self.charmask[y, x]) for x, pixel in enumerate(row))
            )
            sys.stdout.write(s)
        sys.stdout.flush()
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write('\033[0m\033[{};0H\033[?25h'.format(self.rawbuf.shape[0]+3))
        super().__exit__(exc_type, exc_val, exc_tb)


class Terminal(TerminalMonitor, Driver):
    pass

