# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from ugly.virtual import Emulator

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
    # tested working
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.unicornhathd import UnicornHatHD
            return UnicornHatHD()
        except ImportError:
            pass
    return Emulator(16, 16, 3, 8, driver=driver, name='UnicornHatHD')

@device
def unicornhat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.ws2812 import WS2812
            return WS2812(8, 8, serpentine=True, name='UnicornHat')
        except ImportError:
            pass
    return Emulator(8, 8, 3, 8, driver=driver, name='UnicornHat')

@device
def unicornphat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.ws2812 import WS2812
            return WS2812(8, 4, serpentine=True, name='UnicornPhat')
        except ImportError:
            pass
    return Emulator(8, 4, 3, 8, driver=driver, name='UnicornPhat')

@device
def cjmcu8x8(driver='auto'):
    """
    Generic AliExpress 8x8 WS2812 Panel
    """
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.ws2812 import WS2812
            return WS2812(8, 8, serpentine=False, name='CJMCU 8x8')
        except ImportError:
            raise
    return Emulator(8, 8, 3, 8, driver=driver, name='CJMCU 8x8')

@device
def homebrew(driver='auto'):
    """
    DIY holtek panel, 15x7
    """
    if driver == 'native' or driver == 'auto':
        try:
            from ugly.drivers.hardware.ht16k33 import Homebrew
            return Homebrew()
        except ImportError:
            raise
    return Emulator(15, 7, 1, 1, driver=driver, name='Homebrew')

@device
def scrollphathd(driver='auto'):
    if driver == 'native' or driver == 'auto':
        try:
            from ugly.drivers.hardware.is31fl3731 import ScrollPhatHD
            return ScrollPhatHD()
        except ImportError:
            raise
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.scrollphathd import ScrollPhatHD
            return ScrollPhatHD()
        except ImportError:
            pass
    return Emulator(17, 7, 1, 8, driver=driver, name='ScrollPhatHD')

@device
def scrollphat(driver='auto'):
    if driver == 'native' or driver == 'auto':
        try:
            from ugly.drivers.hardware.is31fl3730 import ScrollPhat
            return ScrollPhat()
        except ImportError:
            raise
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.scrollphat import ScrollPhat
            return ScrollPhat()
        except ImportError:
            pass
    return Emulator(11, 5, 1, 1, driver=driver, name='ScrollPhat')

@device
def blinkt(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        try:
            from ugly.drivers.legacy.blinkt import Blinkt
            return Blinkt()
        except ImportError:
            pass
    return Emulator(8, 1, 3, 8, driver=driver, name='Blinkt')

def Display(device, driver='auto'):
    return globals()[device.lower()](driver=driver.lower())
