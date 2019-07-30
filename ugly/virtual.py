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

def Emulator(width, height, channels, depth, driver='auto', name=None):
    """
    Return an emulated device, optionally choosing driver automatically.
    """
    driver = driver.lower()

    rawbuf = np.zeros((height, width, channels), dtype=np.uint8)

    if driver == 'sdl' or driver == 'auto' or driver == 'autoemu':
        try:
            from ugly.drivers.virtual.sdl import SDL
            return SDL(rawbuf, depth, name=name)
        except Exception:
            pass
    if driver == 'terminal' or driver == 'auto' or driver == 'autoemu':
        try:
            from ugly.drivers.virtual.terminal import Terminal
            return Terminal(rawbuf, depth, name=name)
        except ImportError:
            pass
    if driver == 'ffmpeg': # don't select this one automatically
        try:
            from ugly.drivers.virtual.ffmpeg import Ffmpeg
            return Ffmpeg(rawbuf, depth, name=name)
        except ImportError:
            pass
    # If we got here, no emulation drivers were available.
    # TODO: This should raise a custom exception, "No drivers available."
    raise ImportError


def Monitor(device, driver="auto"):
    """
    Return a monitor device, optionally choosing driver automatically.
    """
    driver = driver.lower()
    name = 'Monitor of {}'.format(device.name)

    if driver == 'sdl' or driver == 'auto':
        try:
            from ugly.drivers.virtual.sdl import SDLMonitor
            return SDLMonitor(device.rawbuf, device.depth, name=name)
        except ImportError:
            pass
    if driver == 'terminal' or driver == 'auto':
        try:
            from ugly.drivers.virtual.terminal import TerminalMonitor
            return TerminalMonitor(device.rawbuf, device.depth, name=name)
        except ImportError:
            pass
    if driver == 'ffmpeg': # don't select this one automatically
        try:
            from ugly.drivers.virtual.ffmpeg import FfmpegMonitor
            return FfmpegMonitor(device.rawbuf, device.depth, name=name)
        except ImportError:
            pass
    # If we got here, no emulation drivers were available.
    # TODO: This should raise a custom exception, "No drivers available."
    raise ImportError
