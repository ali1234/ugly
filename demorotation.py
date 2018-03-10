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

import time
import numpy as np

from ugly.devices import Display
from ugly.drivers.base import Virtual

from effects import random_effect, intro_effect
from args import Args

def main():

    args = Args()

    with Display(device=args.device, driver=args.driver) as display:
        monitor = display.connect_monitor(args.monitor)
        
        display.scale = 8

        now = time.monotonic()

        rotori = 0

        try:
            while True:
                start = now
                while now - start < 1.0:
                    now = time.monotonic()

                    if display.channels == 3:
                        display.buffer[:] = intro_effect(display.width, display.height)(now) * 0.75

                        display.pixels[0:2, 0:2] = np.array((0xff, 0, 0))
                        display.pixels[2:6, 0] = np.array((0, 0xff, 0))
                        display.pixels[2:6, 1] = np.array((0, 0, 0))
                        display.pixels[0, 2:8] = np.array((0, 0, 0xff))
                        display.pixels[1, 2:8] = np.array((0, 0, 0))

                    elif display.channels == 1:
                        display.buffer[:,:,0] = (intro_effect(display.width, display.height)(now) * 0.75)[:,:,1]

                    display.show()
                    time.sleep(0.01)
                rotori += 1
                display.rotation = rotori & 3
                if isinstance(display, Virtual):
                    display.orientation = (rotori >> 2) & 3
                display.flip_horizontal = (rotori >> 4) & 1
                display.flip_vertical = (rotori >> 5) & 1


        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
