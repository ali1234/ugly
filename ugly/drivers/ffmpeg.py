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

from ugly.drivers.base import Framebuffer, Virtual

class Ffmpeg(Framebuffer, Virtual):
    """
    Records output to a video file.
    """
    def __init__(self, width, height, channels, depth, scale=8):
        super().__init__(width, height, channels, depth)
        self.__scale = scale
        self.__ffmpeg = subprocess.Popen("ffmpeg -i pipe: -r 30 -pix_fmt yuv420p video.webm".split(), stdin=subprocess.PIPE)

    def show(self):

        # TODO: handle self.rotation and self.physical_rotation

        imbuf = np.repeat(np.repeat(self.buf, self.__scale, axis=0), self.__scale, axis=1)
        for i in range(0, self.width):
            imbuf[:,i*self.__scale,:] = 0
        for i in range(0, self.height):
            imbuf[i*self.__scale,:,:] = 0
        imbuf = np.pad(imbuf, ((0,1), (0,1), (0,1)), mode='wrap')
        Image.fromarray(imbuf).save(self.__ffmpeg.stdin, format='png')

    def off(self):
        self.__ffmpeg.stdin.close()
        self.__ffmpeg.wait()