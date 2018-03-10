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
import sdl2
import sdl2.ext

from ugly.buffer import Drawable
from ugly.drivers.base import Virtual


sdl2.ext.init()
#sdl2.ext.Window.DEFAULTFLAGS = sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_UTILITY

class SDLMonitor(Virtual):
    """
    Emulates a graphics device on the terminal.
    """

    def __enter__(self):
        self.window = sdl2.ext.Window(self.name, size=self._window_size())
        self.window.show()
        return super().__enter__()

    def _window_size(self):
        h = (self.rawbuf.shape[0] * self.scale) + 1
        w = (self.rawbuf.shape[1] * self.scale) + 1
        if self.orientation & 1:
            return (h, w)
        else:
            return (w, h)

    def orientation_changed(self):
        sdl2.SDL_SetWindowSize(self.window.window, *self._window_size())

    def scale_changed(self):
        sdl2.SDL_SetWindowSize(self.window.window, *self._window_size())

    def show(self):
        r = 0
        g = 1%self.channels
        b = 2%self.channels
        if self.depth == 1:
            outbuf = ((self.rawbuf & self.depth) > 0) * 255
        else:
            outbuf = self.rawbuf

        outbuf = np.rot90(outbuf, self.orientation, axes=(0, 1))

        imbuf = np.repeat(np.repeat(outbuf, self.scale, axis=0), self.scale, axis=1)
        for i in range(0, imbuf.shape[0], self.scale):
            imbuf[i,:,:] = 0
        for i in range(0, imbuf.shape[1], self.scale):
            imbuf[:,i,:] = 0
        imbuf = np.pad(imbuf, ((0,1), (0,1), (0,1)), mode='wrap')

        s = np.transpose(sdl2.ext.pixels3d(self.window.get_surface()), (1, 0, 2))
        s[:,:,2] = imbuf[:,:,r]
        s[:,:,1] = imbuf[:,:,g]
        s[:,:,0] = imbuf[:,:,b]
        self.window.refresh()
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)


class SDL(SDLMonitor, Drawable):
    pass

