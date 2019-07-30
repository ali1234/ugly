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

from ugly.devices import Display
from ugly.drivers.base import Virtual

from ugly.demos.effects import random_effect, intro_effect
from ugly.demos.args import Args

def main():

    args = Args()

    with Display(device=args.device, driver=args.driver) as display:
        monitor = display.connect_monitor(args.monitor)

        if isinstance(display, Virtual):
            display.orientation = args.orientation

        if isinstance(monitor, Virtual):
            monitor.orientation = args.orientation

        display.gamma = args.gamma
        display.rotation = args.rotation
        display.flip_horizontal = args.flip_h
        display.flip_vertical = args.flip_v
        display.clear_on_exit = not args.keep

        effect_time = 10  # seconds
        effects_count = 0
        effects_limit = None
        effect = (intro_effect(display.width, display.height), effect_time)
        next_effect = (random_effect(display.width, display.height), effect_time)

        now = time.monotonic()
        start = now

        try:
            while True:

                if args.fixed_timestep:
                    now += 1/30
                else:
                    now = time.monotonic()

                remaining = max(effect[1] - (now - start), 0)

                if display.channels == 3:
                    display.buffer[:] = effect[0](now)
                    if remaining < 1:
                        display.buffer[:] = display.buffer * remaining
                        display.buffer[:] = display.buffer + (next_effect[0](now) * (1-remaining))

                elif display.channels == 1:
                    display.buffer[:,:,0] = effect[0](now)[:,:,1]
                    if remaining < 1:
                        display.buffer[:,:,0] = display.buffer[:,:,0] * remaining
                        display.buffer[:,:,0] = display.buffer[:,:,0] + (next_effect[0](now)[:,:,1] * (1-remaining))

                display.show()

                if remaining == 0:
                    start = now
                    effect = next_effect
                    next_effect = (random_effect(display.width, display.height), effect_time)
                    effects_count += 1
                    if effects_limit is not None and effects_count >= effects_limit:
                        break

                time.sleep(0.001)


        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
