# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

import contextlib

from ugly.virtual import Emulator

devices = {}
def device(f):
    devices[f.__name__] = f
    return f

def GetDevices():
    return sorted(devices.keys())


@contextlib.contextmanager
def probe(driver):
    try:
        yield
    except ImportError:
        if driver == "auto":
            pass
        else:
            raise


# Factories for actual devices.
# Real or emulated depending on selected driver.
# It can autoselect based on what modules are available!

@device
def terminal(driver='terminal'):
    from shutil import get_terminal_size
    size = get_terminal_size((16, 16))
    return Emulator((size.columns-2)//2, size.lines-2, 3, 8, driver='terminal', name='Terminal')

@device
def unicornhathd(driver='auto'):
    # tested working
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.unicornhathd import UnicornHatHD
            return UnicornHatHD()
    return Emulator(16, 16, 3, 8, driver=driver, name='UnicornHatHD')

@device
def unicornhat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.ws2812 import WS2812
            return WS2812(8, 8, serpentine=True, name='UnicornHat')
    return Emulator(8, 8, 3, 8, driver=driver, name='UnicornHat')

@device
def unicornphat(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.ws2812 import WS2812
            return WS2812(8, 4, serpentine=True, name='UnicornPhat')
    return Emulator(8, 4, 3, 8, driver=driver, name='UnicornPhat')

@device
def cjmcu8x8(driver='auto'):
    """
    Generic AliExpress 8x8 WS2812 Panel
    """
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.ws2812 import WS2812
            return WS2812(8, 8, serpentine=False, name='CJMCU 8x8')
    return Emulator(8, 8, 3, 8, driver=driver, name='CJMCU 8x8')

@device
def homebrew(driver='auto'):
    """
    DIY holtek panel, 15x7
    """
    if driver == 'native' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.hardware.ht16k33 import Homebrew
            return Homebrew()
    return Emulator(15, 7, 1, 1, driver=driver, name='Homebrew')

@device
def scrollphathd(driver='auto'):
    if driver == 'native' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.hardware.is31fl3731 import ScrollPhatHD
            return ScrollPhatHD()
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.scrollphathd import ScrollPhatHD
            return ScrollPhatHD()
    return Emulator(17, 7, 1, 8, driver=driver, name='ScrollPhatHD')

@device
def scrollphat(driver='auto'):
    if driver == 'native' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.hardware.is31fl3730 import ScrollPhat
            return ScrollPhat()
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.scrollphat import ScrollPhat
            return ScrollPhat()
    return Emulator(11, 5, 1, 1, driver=driver, name='ScrollPhat')

@device
def blinkt(driver='auto'):
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            from ugly.drivers.legacy.blinkt import Blinkt
            return Blinkt()
    return Emulator(8, 1, 3, 8, driver=driver, name='Blinkt')

@device
def tasbot(driver='auto'):
    from ugly.drivers.legacy.tasbot import TasBot, mask
    if driver == 'legacy' or driver == 'auto':
        with probe(driver):
            return TasBot(led_pin=10)
    return Emulator(28, 8, 3, 8, driver=driver, mask=mask, name='TasBot')

def Display(device, driver='auto'):
    return globals()[device.lower()](driver=driver.lower())
