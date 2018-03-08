# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

import subprocess
import numpy as np
from PIL import Image

from ugly.drivers.base import Base, Monitor, Framebuffer, Virtual

__all__ = ['Ffmpeg', 'FfmpegBase']


class FfmpegBase(Base, Virtual):
    """
    Records output to a video file.
    """

    def __enter__(self):
        self.__scale = 4
        self.__ffmpeg = subprocess.Popen("ffmpeg -y -i pipe: -r 30 -pix_fmt yuv420p video.webm".split(), stdin=subprocess.PIPE)
        return self

    def show(self):

        outbuf = np.rot90(self.buf, self.rotation + self.physical_rotation, axes=(0, 1))

        imbuf = np.repeat(np.repeat(outbuf, self.__scale, axis=0), self.__scale, axis=1)
        for i in range(0, self.width):
            imbuf[:,i*self.__scale,:] = 0
        for i in range(0, self.height):
            imbuf[i*self.__scale,:,:] = 0
        imbuf = np.pad(imbuf, ((0,1), (0,1), (0,1)), mode='wrap')
        Image.fromarray(imbuf).save(self.__ffmpeg.stdin, format='png')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__ffmpeg.stdin.close()
        self.__ffmpeg.wait()


class Ffmpeg(Framebuffer, FfmpegBase):
    pass


class FfmpegMonitor(Monitor, FfmpegBase):
    pass
