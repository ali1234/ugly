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
import sdl2.ext

from ugly.drivers.base import Base, Monitor, Framebuffer, Virtual

__all__ = ['SDL', 'SDLMonitor']


sdl2.ext.init()


class SDLBase(Base, Virtual):
    """
    Emulates a graphics device on the terminal.
    """

    def __enter__(self):
        self.window = sdl2.ext.Window(str(type(self)), size=((self.width*self.scale)+1, (self.height*self.scale)+1))
        self.window.show()
        return self

    def show(self):
        r = 0
        g = 1%self.channels
        b = 2%self.channels
        if self.depth == 1:
            outbuf = ((self.buf & self.depth)>0) * 255
        else:
            outbuf = self.buf

        outbuf = np.rot90(outbuf, self.rotation + self.orientation, axes=(0, 1))

        imbuf = np.repeat(np.repeat(outbuf, self.scale, axis=0), self.scale, axis=1)
        for i in range(0, self.width):
            imbuf[:,i*self.scale,:] = 0
        for i in range(0, self.height):
            imbuf[i*self.scale,:,:] = 0
        imbuf = np.pad(imbuf, ((0,1), (0,1), (0,1)), mode='wrap')

        s = sdl2.ext.pixels3d(self.window.get_surface())
        s[:,:,0] = np.swapaxes(imbuf, 0, 1)[:,:,r]
        s[:,:,1] = np.swapaxes(imbuf, 0, 1)[:,:,g]
        s[:,:,2] = np.swapaxes(imbuf, 0, 1)[:,:,b]
        self.window.refresh()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class SDL(Framebuffer, SDLBase):
    pass


class SDLMonitor(Monitor, SDLBase):
    pass
