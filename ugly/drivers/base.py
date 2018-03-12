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

from ugly.buffer import Buffer
from ugly.virtual import Monitor

class Driver(Buffer):
    """
    Base for devices.
    """

    def __init__(self, rawbuf: np.ndarray, depth: int, name = None):
        super().__init__(rawbuf, depth) # object or Virtual
        self.__monitor = None
        self.__name = name
        self.__gamma = 1
        self.__gammalut = None

    @property
    def name(self):
        if self.__name is None:
            return type(self).__name__
        else:
            return self.__name

    @property
    def gamma(self):
        return self.__gamma

    @gamma.setter
    def gamma(self, g):
        self.__gamma = g
        if g == 1.0:
            self.__gammalut = None
        else:
            self.__gammalut = (((np.arange(0, 256) / 255) ** 2.25) * 255).astype(np.uint8)

    @property
    def gammabuf(self):
        if self.__gammalut is None:
            return self.rawbuf
        else:
            return self.__gammalut.take(self.rawbuf)

    def __enter__(self):
        return self

    def disconnect_monitor(self):
        if self.__monitor:
            self.__monitor.__exit__(None, None, None)
            self.__monitor = None

    def connect_monitor(self, driver="any"):
        if driver is None:
            return None
        self.disconnect_monitor()
        self.__monitor = Monitor(self, driver).__enter__()
        return self.__monitor

    def show(self):
        if self.__monitor:
            self.__monitor.show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_monitor()



class Virtual(Driver):
    """
    Base for virtual devices which are not backed by physical hardware.
    Provides emulation of physical properties.
    """

    def __init__(self, rawbuf: np.ndarray, depth: int, name = None):
        super().__init__(rawbuf, depth, name)
        self.__orientation = 0
        self.__scale = 16

    def convert_buffer(self):
        """
        Helper to convert buffer for display.
        """
        if self.depth == 1:
            outbuf = ((self.gammabuf & 0x80) > 0) * 255
        else:
            outbuf = self.gammabuf

        return np.rot90(outbuf, self.orientation, axes=(0, 1))

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, orientation: int):
        t = orientation % 4
        if self.__orientation != t:
            self.__orientation = t
            self.orientation_changed()

    def orientation_changed(self):
        """
        Override this if you need to forward rotation events some place.
        """
        pass

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale: int):
        if scale != self.__scale:
            self.__scale = scale
            self.scale_changed()

    def scale_changed(self):
        pass
