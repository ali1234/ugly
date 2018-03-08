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

    from ugly.devices import Display, GetDevices
    from ugly.drivers.base import Virtual

    with Display(device='UnicornHatHD', driver='sdl', monitor=None) as display:
        with Display(device='UnicornHat', driver='sdl', monitor=None) as dtl:
            with Display(device='UnicornHat', driver='sdl', monitor=None) as dtr:
                with Display(device='UnicornHat', driver='sdl', monitor=None) as dbl:
                    with Display(device='UnicornHat', driver='sdl', monitor=None) as dbr:

                        effect_time = 10  # seconds
                        effects_count = 0
                        effects_limit = None
                        effects = [
                            (intro_effect(display.width, display.height), effect_time),
                            (random_effect(display.width, display.height), effect_time),
                        ]

                        display.rotation = 2

                        if isinstance(display, Virtual):
                            display.orientation = 2

                        now = time.monotonic()

                        try:
                            while True:
                                start = now
                                while True:
                                    now = time.monotonic()
                                    remaining = effects[0][1] - (now - start)
                                    if remaining < 0:
                                        remaining = 0
                                    if display.channels == 3:
                                        display.buf[:] = effects[0][0](now)
                                        if remaining < 1:
                                            display.buf[:] = display.buf * remaining
                                            display.buf[:] = display.buf + (effects[1][0](now) * (1-remaining))
                                    elif display.channels == 1:
                                        display.buf[:,:,0] = effects[0][0](now)[:,:,1]
                                        if remaining < 1:
                                            display.buf[:,:,0] = display.buf[:,:,0] * remaining
                                            display.buf[:,:,0] = display.buf[:,:,0] + (effects[1][0](now)[:,:,1] * (1-remaining))

                                    dtl.buf[:] = display.buf[0:8,0:8,:]
                                    dtr.buf[:] = display.buf[0:8,8:16,:]
                                    dbl.buf[:] = display.buf[8:16,0:8,:]
                                    dbr.buf[:] = display.buf[8:16,8:16,:]

                                    display.show()
                                    dtl.show()
                                    dtr.show()
                                    dbl.show()
                                    dbr.show()

                                    if remaining == 0:
                                        break

                                    time.sleep(0.001)

                                effect = effects.pop(0)
                                effects.append((random_effect(display.width, display.height), effect_time))
                                effects_count += 1
                                if effects_limit is not None and effects_count >= effects_limit:
                                    break

                        except KeyboardInterrupt:
                            pass

if __name__ == '__main__':
    main()
