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
    Provides emulation of physical properties, like rotation.
    """

    def __init__(self):
        self.__physical_rotation = 0

    @property
    def physical_rotation(self):
        return self.__physical_rotation

    @physical_rotation.setter
    def physical_rotation(self, rotation: int):
        self.__physical_rotation = rotation % 4



class Framebuffer(Base):
    """
    Base for drivers which must manage their own internal framebuffer.
    """

    def __init__(self, width: int, height: int, channels: int, depth: int):
        super().__init__(np.zeros((height, width, channels), dtype=np.uint8), depth)
