#!/usr/bin/env python3

# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from effects import random_effect, intro_effect

def main():

    import time, argparse

    from ugly.virtual import Emulator
    from ugly.drivers.base import Virtual

    with Emulator(32, 16, 3, 8) as display:

        display.scale = 8

        now = time.monotonic()

        rotori = 0

        try:
            while True:
                start = now
                while now - start < 1.0:
                    now = time.monotonic()
                    display.buf[:] = intro_effect(display.width, display.height)(now)

                    display.show()
                    time.sleep(0.01)
                rotori += 1
                display.rotation = rotori & 3
                display.orientation = (rotori >> 2) & 3

        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
