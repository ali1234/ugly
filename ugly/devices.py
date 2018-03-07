# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from ugly.drivers.legacy import Legacy
from ugly.emulator import Emulator

# Factories for actual devices.
# Real or emulated depending on selected driver.
# It can autoselect based on what modules are available!

def UnicornHatHD(driver=None):
    if driver == 'legacy' or driver == None:
        try:
            import unicornhathd
            return Legacy(unicornhathd, 8)
        except ImportError:
            pass
    return Emulator(16, 16, 3, 0, driver=driver)


def UnicornHat(driver=None):
    if driver == 'legacy' or driver == None:
        try:
            import unicornhat
            return Legacy(unicornhat, 8)
        except ImportError:
            pass
    return Emulator(8, 8, 3, 0, driver=driver)


def UnicornPhat(driver=None):
    if driver == 'legacy' or driver == None:
        try:
            import unicornhat
            return Legacy(unicornhat, 8)
        except ImportError:
            pass
    return Emulator(8, 4, 3, 0, driver=driver)


def ScrollPhatHD(driver=None):
    if driver == 'legacy' or driver == None:
        try:
            import scrollphathd
            return Legacy(scrollphathd, 8)
        except ImportError:
            pass
    return Emulator(17, 7, 1, 0, driver=driver)


def ScrollPhat(driver=None):
    if driver == 'legacy' or driver == None:
        try:
            import scrollphat
            return Legacy(scrollphat, 1)
        except ImportError:
            pass
    return Emulator(11, 5, 1, 1, driver=driver)


def Blinkt(driver=None):
    if driver == 'legacy' or driver == None:
        try:
            import blinkt
            return Legacy(blinkt, 8)
        except ImportError:
            pass
    return Emulator(8, 1, 3, 8, driver=driver)