# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from importlib import import_module

from ugly.drivers.legacy import Legacy
from ugly.virtual import Emulator, Monitor

devices = {}
def device(f):
    devices[f.__name__] = f
    return f

def GetDevices():
    return sorted(devices.keys())

# Factories for actual devices.
# Real or emulated depending on selected driver.
# It can autoselect based on what modules are available!

@device
def unicornhathd(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            import unicornhathd
            return Legacy(unicornhathd, unicornhathd._buf, 8, 'UnicornHatHD')
        except ImportError:
            pass
    return Emulator(16, 16, 3, 8, driver=driver, name='UnicornHatHD')

@device
def unicornhat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            import unicornhat
            return Legacy(unicornhat, unicornhat._buf, 8, 'UnicornHat')
        except ImportError:
            pass
    return Emulator(8, 8, 3, 8, driver=driver, name='UnicornHat')

@device
def unicornphat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            import unicornhat
            return Legacy(unicornhat, unicornhat._buf[:4,:,:], 8, 'UnicornPhat')
        except ImportError:
            pass
    return Emulator(8, 4, 3, 8, driver=driver, name='UnicornPhat')

@device
def scrollphathd(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            import scrollphathd
            return Legacy(scrollphathd, scrollphathd.buffer, 8, 'ScrollPhatHD')
        except ImportError:
            pass
    return Emulator(17, 7, 1, 8, driver=driver, name='ScrollPhatHD')

@device
def scrollphat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            import scrollphat
            return Legacy(scrollphat, scrollphat.buffer, 1, 'ScrollPhat')
        except ImportError:
            pass
    return Emulator(11, 5, 1, 1, driver=driver, name='ScrollPhat')

@device
def blinkt(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            import blinkt
            return Legacy(blinkt, blinkt._buf, 8, 'Blinkt')
        except ImportError:
            pass
    return Emulator(8, 1, 3, 8, driver=driver, name='Blinkt')

def Display(device, driver='auto'):
    return globals()[device.lower()](driver=driver.lower())
