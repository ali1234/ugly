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

from ugly.drivers.base import Base, Monitor, Framebuffer, Virtual

__all__ = ['Terminal', 'TerminalMonitor']


class TerminalBase(Base, Virtual):
    """
    Emulates a graphics device on the terminal.
    """

    def __enter__(self):
        sys.stdout.write('\033[2J\033[?25l')
        return self

    def show(self):
        r = 0
        g = 1%self.channels
        b = 2%self.channels
        if self.depth == 1:
            outbuf = ((self.buf & self.depth)>0) * 255
        else:
            outbuf = self.buf

        outbuf = np.rot90(outbuf, self.rotation+self.physical_rotation, axes=(0, 1))

        for n, row in enumerate(outbuf):
            sys.stdout.write('\033[{};0H'.format(n+2))
            s = ' '.join(
                ('\033[38;2;{:d};{:d};{:d}m\u25cf'.format(pixel[r], pixel[g], pixel[b]) for pixel in row)
            )
            sys.stdout.write('  ')
            sys.stdout.write(s)
        sys.stdout.flush()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write('\033[0m\033[{};0H\033[?25h'.format(self.height+3))


class Terminal(Framebuffer, TerminalBase):
    pass


class TerminalMonitor(Monitor, TerminalBase):
    pass
