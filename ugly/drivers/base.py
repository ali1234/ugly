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


class Base(object):
    """
    Base for all graphics drivers.
    """

    def __init__(self, buf: np.ndarray, depth: int):
        super().__init__()
        self.__buf = buf
        self.__depth = depth
        self.__rotation = 0

    @property
    def buf(self):
        return self.__buf

    @property
    def width(self):
        return self.__buf.shape[1]

    @property
    def height(self):
        return self.__buf.shape[0]

    @property
    def channels(self):
        return self.__buf.shape[2]

    @property
    def depth(self):
        return self.__depth

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation: int):
        self.__rotation = rotation % 4
        self.rotation_changed()

    def rotation_changed(self):
        """
        Override this if you need to forward rotation events some place.
        """
        pass


class Virtual(object):
    """
    Base for virtual drivers which are not backed by physical hardware.
    Provides emulation of physical properties, like orientation.
    """

    def __init__(self):
        self.__orientation = 0
        self.__scale = 16

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, orientation: int):
        self.__orientation = orientation % 4
        self.orientation_changed()

    def orientation_changed(self):
        """
        Override this if you need to forward rotation events some place.
        """
        pass

    @property
    def scale(self):
        return self.__scale


class Framebuffer(Base):
    """
    Base for drivers which must manage their own internal framebuffer.
    """

    def __init__(self, width: int, height: int, channels: int, depth: int):
        super().__init__(np.zeros((height, width, channels), dtype=np.uint8), depth)


class Monitor(Base):
    """
    Base for a virtual device which monitors (mirrors) another device.
    """

    def __init__(self, device):
        super().__init__(device.buf, device.depth)
        self.__device = device
        self.__rotation = self.__device.rotation

    def __enter__(self):
        self.__device.__enter__()
        super().__enter__()
        return self

    def rotation_changed(self):
        self.__device.rotation = self.__rotation

    def show(self):
        super().show()
        self.__device.show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.__device.__exit__(exc_type, exc_val, exc_tb)
