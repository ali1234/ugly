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

from ugly.buffer import Drawable
from ugly.drivers.base import Driver, Virtual


class FfmpegMonitor(Driver, Virtual):
    """
    Records output to a video file.
    """

    def __enter__(self):
        self.__ffmpeg = subprocess.Popen("ffmpeg -y -i pipe: -r 30 -pix_fmt yuv420p video.webm".split(), stdin=subprocess.PIPE)
        return super().__enter__()

    def show(self):

        outbuf = np.rot90(self.rawbuf, self.orientation, axes=(0, 1))

        imbuf = np.repeat(np.repeat(outbuf, self.scale, axis=0), self.scale, axis=1)
        for i in range(0, self.rawbuf.shape[1]):
            imbuf[:,i*self.scale,:] = 0
        for i in range(0, self.rawbuf.shape[0]):
            imbuf[i*self.scale,:,:] = 0
        imbuf = np.pad(imbuf, ((0,1), (0,1), (0,1)), mode='wrap')
        Image.fromarray(imbuf).save(self.__ffmpeg.stdin, format='png')
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__ffmpeg.stdin.close()
        self.__ffmpeg.wait()
        super().__exit__(exc_type, exc_val, exc_tb)


class Ffmpeg(FfmpegMonitor, Drawable):
    pass

