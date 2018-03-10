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

    with Display(device=args.device, driver=args.driver, monitor=args.monitor) as display:

        effect_time = 10  # seconds
        effects_count = 0
        effects_limit = None
        effects = [
            (intro_effect(display.width, display.height), effect_time),
            (random_effect(display.width, display.height), effect_time),
        ]

        print (args.rotation)

        display.rotation = args.rotation

        if isinstance(display, Virtual):
            display.orientation = args.orientation

        now = time.monotonic()

        try:
            while True:
                start = now
                while True:
                    if args.fixed_timestep:
                        now += 1/30
                    else:
                        now = time.monotonic()
                    remaining = effects[0][1] - (now - start)
                    if remaining < 0:
                        remaining = 0
                    if display.channels == 3:
                        display.buffer[:] = effects[0][0](now)
                        if remaining < 1:
                            display.buffer[:] = display.buffer * remaining
                            display.buffer[:] = display.buffer + (effects[1][0](now) * (1-remaining))
                    elif display.channels == 1:
                        display.buffer[:,:,0] = effects[0][0](now)[:,:,1]
                        if remaining < 1:
                            display.buffer[:,:,0] = display.buffer[:,:,0] * remaining
                            display.buffer[:,:,0] = display.buffer[:,:,0] + (effects[1][0](now)[:,:,1] * (1-remaining))

                    display.show()
                    if remaining == 0:
                        break

                    time.sleep(0.001)

                effects.pop(0)
                effects.append((random_effect(display.width, display.height), effect_time))
                effects_count += 1
                if effects_limit is not None and effects_count >= effects_limit:
                    break

        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
