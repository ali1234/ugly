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


def legacy(modname, depth, wrapper=Legacy, monitor=None):
    m = import_module(modname)
    if monitor is None:
        return wrapper(m)
    else:
        return Monitor(wrapper(m), driver=monitor)

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
def UnicornHatHD(driver='auto', monitor=None):
    if driver == 'legacy' or driver == 'auto':
        try:
            return legacy('unicornhathd', 8, monitor=monitor)
        except ImportError:
            pass
    return Emulator(16, 16, 3, 8, driver=driver)

@device
def UnicornHat(driver='auto', monitor=None):
    if driver == 'legacy' or driver == 'auto':
        try:
            return legacy('unicornhat', 8, monitor=monitor)
        except ImportError:
            pass
    return Emulator(8, 8, 3, 8, driver=driver)

@device
def UnicornPhat(driver='auto', monitor=None):
    if driver == 'legacy' or driver == 'auto':
        try:
            return legacy('unicornhat', 8, monitor=monitor)
        except ImportError:
            pass
    return Emulator(8, 4, 3, 8, driver=driver)

@device
def ScrollPhatHD(driver='auto', monitor=None):
    if driver == 'legacy' or driver == 'auto':
        try:
            return legacy('scrollphathd', 8, monitor=monitor)
        except ImportError:
            pass
    return Emulator(17, 7, 1, 8, driver=driver)

@device
def ScrollPhat(driver='auto', monitor=None):
    if driver == 'legacy' or driver == 'auto':
        try:
            return legacy('scrollphat', 1, monitor=monitor)
        except ImportError:
            pass
    return Emulator(11, 5, 1, 1, driver=driver)

@device
def Blinkt(driver='auto', monitor=None):
    if driver == 'legacy' or driver == 'auto':
        try:
            import blinkt
            return legacy('blinkt', 8, monitor=monitor)
        except ImportError:
            pass
    return Emulator(8, 1, 3, 8, driver=driver)

def Display(device, driver='auto', monitor=None):
    return globals()[device](driver=driver, monitor=monitor)
