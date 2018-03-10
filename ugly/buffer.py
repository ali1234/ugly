
import numpy as np


class Buffer(object):

    def __init__(self, rawbuf: np.ndarray, depth: int):
        super().__init__()
        self.__rawbuf = rawbuf
        self.__depth = depth

    @property
    def rawbuf(self):
        return self.__rawbuf

    @property
    def channels(self):
        return self.__rawbuf.shape[2]

    @property
    def depth(self):
        return self.__depth


class Drawable(Buffer):

    def __init__(self, rawbuf: np.ndarray, depth: int):
        super().__init__(rawbuf, depth)
        self.__rotation = 0

    @property
    def buffer(self):
        """A rotated view into _buf with [y, x] ordering."""
        return np.rot90(self.rawbuf, self.rotation)

    @property
    def pixels(self):
        """A rotated view into _buf with [x, y] ordering."""
        return np.transpose(self.buffer, (1, 0, 2))

    @property
    def width(self):
        return self.buffer.shape[1]

    @property
    def height(self):
        return self.buffer.shape[0]

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation: int):
        self.__rotation = rotation % 4
