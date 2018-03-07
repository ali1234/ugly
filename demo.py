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


import time, math, random

import numpy as np

# Here just import whichever display you want to use
# This could be autodetected if the hardware supports it
from ugly.devices import UnicornHatHD as Display
from ugly.drivers.base import Virtual

display = Display(driver=None) # autodetect driver

display.rotation = 2

if isinstance(display, Virtual):
    # Yes, i know what you are going to say. i should make all displays
    # have this property whether they are virtual or not.
    # But that just seems wrong to me. Attempting to set physical rotation
    # on real hardware means the programmer made a mistake.
    display.physical_rotation = 2

# After this point nothing much interesting happens in terms of the class stuff.
# It is all bit twiddling graphics effects. :)

# The key point is that all the following code will run on any device, real or
# emulated. All you have to change is which one you import.
# (Or import an autodetecting factory.)


# helper functions

def distance_from_centre(dx = 0, dy = 0):
    ox = dx + ((display.width/2) - 0.5)
    oy = dy + ((display.height/2) - 0.5)
    # nasty hack warning: the +1 here is to make it work with blinkt which is 1 pixel tall
    x = np.squeeze(np.arange(0, display.width+1, dtype=np.float)[:, np.newaxis] - ox)
    y = np.squeeze(np.arange(0, display.height+1, dtype=np.float)[:, np.newaxis] - oy)
    return x[:-1], y[:-1]

def solid(a):
    s = np.array([[a]], dtype=np.float)
    def _solid(t):
        return s
    return _solid

def cycle(t):
    return np.array([[t*0.2]], dtype=np.float)


# RGB effects

matrix_buf = np.random.randint(0, 0x10f, (display.height, display.width), dtype=np.int16)
matrix_t = 0
def matrix(t):
    global matrix_buf, matrix_t
    matrix_buf = matrix_buf + (np.random.randint(-4, 6, (display.height, display.width), dtype=np.int16))
    if t - matrix_t > 0.05:
        fall = matrix_buf > 0xff
        subs = fall * np.random.randint(0x7f, 0x17f, (display.height, display.width), dtype=np.int16)
        adds = np.roll(subs, 1, axis=0) * 0.75
        adds[0, :] = (np.random.randint(0, 64, (1, display.width), dtype=np.uint8) == 0) * 0xff
        matrix_buf = matrix_buf + adds - subs
        matrix_t = t
    return np.clip(np.stack([matrix_buf-0xff, matrix_buf, matrix_buf-0xff], axis=-1), 0, 0xff)


# boolean effects

def checker(t):
    x, y = distance_from_centre(dx = math.sin(t * 1.333) * display.width, dy = math.cos(t * 2.0) * display.width)
    sc = (math.cos(-t*0.75)) + 2.0
    s = math.sin(t);
    c = math.cos(t);
    xs = ((x * c - y[:, np.newaxis] * s) - math.sin(t / 2.0) * 0.1) / sc;
    ys = ((x * s + y[:, np.newaxis] * c) - math.cos(t / 2.0) * 0.1) / sc;
    return (np.sin(xs) > 0) ^ (np.cos(ys) > 0)

def beams(nbeams = None):
    if nbeams is None:
        nbeams = random.choice([3, 5, 6])
    m = 2 * math.pi / nbeams
    s = 3 / nbeams
    def _beams(t):
        x, y = distance_from_centre(dx = math.sin(t * 3.2) * 3.0, dy = math.cos(t * 1.5) * 3.0)
        return (np.mod(np.arctan2(x, y[:, np.newaxis]) + (math.pi) + t, m) - s) > 0
    return _beams

def zoomrings(t):
    x, y = distance_from_centre(dx = math.sin(t * 3.2) * 3.0, dy = math.cos(t * 1.5) * 3.0)
    return (np.mod(np.sqrt((x**2) + (y**2)[:, np.newaxis])-(t*10), 10) - 5) > 0

_roni = np.unpackbits(np.array([255, 255, 254, 127, 252,  63, 225, 135, 193, 131, 192,   3, 192,
     3, 199, 227, 229, 163, 247, 231, 240,  39, 243, 135, 224,  15,
     240,  31, 253, 127, 255, 255], dtype=np.uint8)).reshape(16, 16) > 0
def roni(t):
    if display.width == 16 and display.height == 16:
        return _roni
    else:
        return np.array([[True]], dtype=np.bool)

def metaballs(num=5):
    dt = np.random.ranf((1, num))*15.0
    sx = np.random.ranf((1, num))*2.0+1.5
    sy = np.random.ranf((1, num))*2.0+1.5
    def _metaballs(t):
        x, y = distance_from_centre(dx=np.sin(sx*t+dt)*6, dy=np.cos(sy*t+dt)*6)
        return np.sum(1 / np.sqrt((x**2) + (y**2)[:, np.newaxis]), axis=-1) > 0.9
    return _metaballs

life_buf = np.random.randint(0, 255, (display.height+2, display.width), dtype=np.uint8) == 0
life_t = 0
def life(t):
    global life_buf, life_t
    if t - life_t > 0.05:
        life_buf = np.roll(life_buf, -1, axis=0)
        life_buf[-1] = np.random.randint(0, 3, (1, display.width), dtype=np.uint8) == 0
        hneighbours = np.roll(life_buf, 1, axis=0)*1 + life_buf*1 + np.roll(life_buf, -1, axis=0)*1
        neighbours = np.roll(hneighbours, 1, axis=1)*1 + hneighbours*1 + np.roll(hneighbours, -1, axis=1)*1 - life_buf
        life_buf = life_buf & (neighbours > 1) & (neighbours < 4)
        life_buf = life_buf | (neighbours == 3)
        life_t = t
    return life_buf[2:]


# grey effects

tinylife_buf = np.random.randint(0, 255, ((display.height*4)+2, display.width*4), dtype=np.uint8) == 0
tinylife_t = 0
def tinylife(t):
    global tinylife_buf, tinylife_t
    if t - tinylife_t > 0.02:
        tinylife_buf = np.roll(tinylife_buf, 1, axis=0)
        tinylife_buf[0] = np.random.randint(0, 3, (1, (display.width*4)), dtype=np.uint8) == 0
        hneighbours = np.roll(tinylife_buf, 1, axis=0)*1 + tinylife_buf*1 + np.roll(tinylife_buf, -1, axis=0)*1
        neighbours = np.roll(hneighbours, 1, axis=1)*1 + hneighbours*1 + np.roll(hneighbours, -1, axis=1)*1 - tinylife_buf
        tinylife_buf = tinylife_buf & (neighbours > 1) & (neighbours < 4)
        tinylife_buf = tinylife_buf | (neighbours == 3)
        tinylife_t = t
    return np.sum(np.sum(tinylife_buf[:-2].reshape(display.height, 4, display.width, 4), axis=3), axis=1) / 8

def rings(t):
    x, y = distance_from_centre(dx = math.sin(t * 2.0) * display.width, dy = math.cos(t * 3.0) * display.width)
    sc = (math.cos(t * 5.0) * 10.0) + 20.0
    return np.mod(np.sqrt((x**2) + (y**2)[:, np.newaxis])/sc, 1)

def swirl(t):
    x, y = distance_from_centre()
    dist = (np.sqrt((x**2) + (y**2)[:, np.newaxis]) * (0.5 + (0.2*math.sin(t*0.5)))) + (-t * 5)
    s = np.sin(dist);
    c = np.cos(dist);
    xs = x * c - y[:, np.newaxis] * s;
    ys = x * s + y[:, np.newaxis] * c;
    return np.mod((np.abs(xs + ys) * 0.05) + (0.1 * t), 1)

def tunnel(nbeams=None):
    b = beams(nbeams)
    def _tunnel(t):
        return (zoomrings(t) * 0.45) + (b(t) * 0.45) + 0.1
    return _tunnel

wind_buf = np.random.randint(0, 6, (display.height, display.width), dtype=np.uint8) == 0
wind_acc_buf = np.zeros((display.height, display.width), dtype=np.float)
wind_t = 0
def wind(t):
    global wind_buf, wind_acc_buf, wind_t
    if t - wind_t > 0.02:
        wind_buf = np.roll(wind_buf, 1, axis=1)
        wind_buf[:,0] = (np.random.randint(0, 6, (display.height,), dtype=np.uint8) == 0)
        wind_acc_buf = np.clip((wind_acc_buf - 0.1), 0, 1) + wind_buf
        wind_t = t
        wind_acc_buf = np.clip(wind_acc_buf, 0.1, 1.0)
    return wind_acc_buf

diamonds_buf = np.random.randint(0, 8, (display.height, display.width), dtype=np.uint16)
diamonds_t = 0
def diamonds(t):
    global diamonds_buf, diamonds_t
    if t - diamonds_t > 0.05:
        diamonds_buf = np.amax(np.stack([
            diamonds_buf,
            np.roll(diamonds_buf, 1, axis=0),
            np.roll(diamonds_buf, -1, axis=0),
            np.roll(diamonds_buf, 1, axis=1),
            np.roll(diamonds_buf, -1, axis=1)
        ]), axis=0)
        diamonds_buf[random.randint(0, display.height-1), random.randint(0, display.width-1)] += 1
        if np.all(diamonds_buf > 256):
            diamonds_buf = diamonds_buf - 256
        diamonds_t = t
    return (diamonds_buf & 0x3) / 3


# colorspace conversions

def grey_to_rgb(grey, r=0, g=0.333, b=0.666, x=0.333, y=0.5, z=6):
    t = grey[:, :, np.newaxis] + np.array([r, g, b])[np.newaxis, np.newaxis, :]
    return np.clip((x - np.abs(np.mod(t, 1)-y))*z, 0, 1) * 255

def hue(grey_func):
    def _hue(t):
        return grey_to_rgb(grey_func(t))
    return _hue

def trippy(grey_func):
    def _trippy(t):
        return grey_to_rgb(grey_func(t), 0, 0.333+math.sin(t), 0.666-math.sin(t))
    return _trippy

def rgb_bars(grey_func):
    def _rgb_bars(t):
        return grey_to_rgb(grey_func(t), z=3)
    return _rgb_bars

# misc

def triple_grey_to_rgb(ga, gb, gc, offa=lambda t: t, offb=lambda t: t, offc=lambda t: t):
    def _triple_grey_to_rgb(t):
        return np.stack([ga(offa(t)), gb(offb(t)), gc(offc(t))], axis=-1)*255
    return _triple_grey_to_rgb

def chromatic_aberration(grey):
    return triple_grey_to_rgb(grey, grey, grey, offa=lambda t: t+(math.sin(t)*0.075), offc=lambda t: t-(math.sin(t)*0.075))


# operators

def multiply(a, b):
    def _multiply(t):
        return a(t) * b(t)[:,:,np.newaxis]
    return _multiply

def invert(a):
    def _invert(t):
        return ~a(t)
    return _invert

def shift(a):
    def _shift(t):
        return a(t)+0.5
    return _shift

def add(a, b):
    def _add(t):
        return a(t) + b(t)
    return _add


# choose a random effect

def random_ca():
    mask = random.choice([checker, zoomrings, beams(), metaballs()])
    return chromatic_aberration(mask)

def random_mult():
    grey = random.choice([swirl, rings])
    colr = random.choice([hue, trippy])
    mask = random.choice([checker, diamonds, tunnel(), zoomrings, beams(), life, tinylife, wind, metaballs()])
    return multiply(colr(grey), mask)

def random_invert_mult():
    # functions are composable in complex ways but on the small screen
    # it mostly ends up looking messy if too much stuff is going on
    grey = random.choice([swirl])
    colr = random.choice([hue, trippy])
    if random.choice([True, False]):
        mask = random.choice([zoomrings, beams()])
        return add(multiply(colr(grey), mask), multiply(colr(shift(grey)), invert(mask)))
    else:
        mask = random.choice([life, metaballs()])
        return multiply(colr(grey), invert(mask))

def random_matrix():
    if random.randint(0,4) == 0:
        return multiply(matrix, roni)
    else:
        return matrix

def random_simple():
    grey = random.choice([swirl, rings])
    colour = random.choice([hue, trippy])
    return colour(grey)

def random_effect():
    return random.choice([
        random_ca,
        random_mult,
        random_mult,
        random_matrix,
        random_simple
    ])()





# playlist

effect_time = 10 # seconds
effects_count = 0
effects_limit = None
effects = [
    (multiply(hue(rings), roni), effect_time),
    (random_effect(), effect_time),
]


# main loop

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

            display.show()
            if remaining == 0:
                break

            time.sleep(0.001)

        effect = effects.pop(0)
        effects.append((random_effect(), effect_time))
        effects_count += 1
        if effects_limit is not None and effects_count >= effects_limit:
            break
except KeyboardInterrupt:
    pass
except Exception as e:
    raise
finally:
    display.off()
