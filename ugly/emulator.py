# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.


def Emulator(width, height, channels, depth, driver=None):
    """
    Return an emulated device, optionally choosing driver automatically.
    """
    if driver == 'terminal' or driver == None:
        try:
            from ugly.drivers.terminal import Terminal
            return Terminal(width, height, channels, depth)
        except ImportError:
            pass
    if driver == 'ffmpeg': # don't select this one automatically
        try:
            from ugly.drivers.ffmpeg import Ffmpeg
            return Ffmpeg(width, height, channels, depth)
        except ImportError:
            pass
    # If we got here, no emulation drivers were available.
    # TODO: This should raise a custom exception, "No drivers available."
    raise ImportError