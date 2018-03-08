# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.


import math, random
import numpy as np

# helper functions

def Solid(a):
    s = np.array([[a]], dtype=np.float)
    def _solid(t):
        return s
    return _solid

def Cycle(t):
    return np.array([[t*0.2]], dtype=np.float)


class Effect(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def distance_from_centre(self, dx=0, dy=0):
        ox = dx + ((self.width / 2) - 0.5)
        oy = dy + ((self.height / 2) - 0.5)
        # nasty hack warning: the +1 here is to make it work with blinkt which is 1 pixel tall
        x = np.squeeze(np.arange(0, self.width + 1, dtype=np.float)[:, np.newaxis] - ox)
        y = np.squeeze(np.arange(0, self.height + 1, dtype=np.float)[:, np.newaxis] - oy)
        return x[:-1], y[:-1]


# RGB effects

class Matrix(Effect):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.t = 0
        self.buf = np.random.randint(0, 0x10f, (height, width), dtype=np.int16)

    def __call__(self, t):
        if t - self.t > 0.05:
            self.buf = self.buf + (np.random.randint(-4, 6, (self.height, self.width), dtype=np.int16))
            fall = self.buf > 0xff
            subs = fall * np.random.randint(0x7f, 0x17f, (self.height, self.width), dtype=np.int16)
            adds = np.roll(subs, 1, axis=0) * 0.75
            adds[0, :] = (np.random.randint(0, 64, (1, self.width), dtype=np.uint8) == 0) * 0xff
            self.buf = self.buf + adds - subs
            self.t = t
        return np.clip(np.stack([self.buf-0xff, self.buf, self.buf-0xff], axis=-1), 0, 0xff)


# boolean effects

class Checker(Effect):

    def __call__(self, t):
        x, y = self.distance_from_centre(dx = math.sin(t * 1.333) * 12.0, dy = math.cos(t * 2.0) * 12.0)
        sc = (math.cos(-t*0.75)) + 2.0
        s = math.sin(t)
        c = math.cos(t)
        xs = ((x * c - y[:, np.newaxis] * s) - math.sin(t / 2.0) * 0.1) / sc
        ys = ((x * s + y[:, np.newaxis] * c) - math.cos(t / 2.0) * 0.1) / sc
        return (np.sin(xs) > 0) ^ (np.cos(ys) > 0)


class Beams(Effect):

    def __init__(self, width, height, nbeams=None):
        super().__init__(width, height)
        if nbeams is None:
            self.nbeams = random.choice([3, 5, 6])
        self.m = 2 * math.pi / self.nbeams
        self.s = 3 / self.nbeams

    def __call__(self, t):
        x, y = self.distance_from_centre(dx = math.sin(t * 3.2) * 3.0, dy = math.cos(t * 1.5) * 3.0)
        return (np.mod(np.arctan2(x, y[:, np.newaxis]) + (math.pi) + t, self.m) - self.s) > 0


class ZoomRings(Effect):

    def __call__(self, t):
        x, y = self.distance_from_centre(dx = math.sin(t * 3.2) * 3.0, dy = math.cos(t * 1.5) * 3.0)
        return (np.mod(np.sqrt((x**2) + (y**2)[:, np.newaxis])-(t*10), 10) - 5) > 0


class Roni(Effect):

    roni = np.unpackbits(np.array([255, 255, 254, 127, 252,  63, 225, 135, 193, 131, 192,   3, 192,
                                     3, 199, 227, 229, 163, 247, 231, 240,  39, 243, 135, 224,  15,
                                   240,  31, 253, 127, 255, 255], dtype=np.uint8)).reshape(16, 16) > 0

    def __call__(self, t):
        if self.width == 16 and self.height == 16:
            return self.roni
        else:
            return np.array([[True]], dtype=np.bool)


class Metaballs(Effect):
    def __init__(self, width, height, num=5):
        super().__init__(width, height)
        self.num = num
        self.dt = np.random.ranf((1, num))*15.0
        self.sx = np.random.ranf((1, num))*2.0+1.5
        self.sy = np.random.ranf((1, num))*2.0+1.5

    def __call__(self, t):
        x, y = self.distance_from_centre(dx=np.sin(self.sx*t+self.dt)*6, dy=np.cos(self.sy*t+self.dt)*6)
        return np.sum(1 / np.sqrt((x**2) + (y**2)[:, np.newaxis]), axis=-1) > 0.9


class Life(Effect):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.t = 0
        self.buf = np.random.randint(0, 255, (self.height+2, self.width), dtype=np.uint8) == 0

    def __call__(self, t):
        if t - self.t > 0.05:
            self.buf = np.roll(self.buf, -1, axis=0)
            self.buf[-1] = np.random.randint(0, 3, (1, self.width), dtype=np.uint8) == 0
            hneighbours = np.roll(self.buf, 1, axis=0)*1 + self.buf*1 + np.roll(self.buf, -1, axis=0)*1
            neighbours = np.roll(hneighbours, 1, axis=1)*1 + hneighbours*1 + np.roll(hneighbours, -1, axis=1)*1 - self.buf
            self.buf = self.buf & (neighbours > 1) & (neighbours < 4)
            self.buf = self.buf | (neighbours == 3)
            self.t = t
        return self.buf[2:]


# grey effects

class TinyLife(Effect):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.t = 0
        self.buf = np.random.randint(0, 255, ((self.height*4)+2, self.width*4), dtype=np.uint8) == 0

    def __call__(self, t):
        if t - self.t > 0.02:
            self.buf = np.roll(self.buf, 1, axis=0)
            self.buf[0] = np.random.randint(0, 3, (1, (self.width*4)), dtype=np.uint8) == 0
            hneighbours = np.roll(self.buf, 1, axis=0)*1 + self.buf*1 + np.roll(self.buf, -1, axis=0)*1
            neighbours = np.roll(hneighbours, 1, axis=1)*1 + hneighbours*1 + np.roll(hneighbours, -1, axis=1)*1 - self.buf
            self.buf = self.buf & (neighbours > 1) & (neighbours < 4)
            self.buf = self.buf | (neighbours == 3)
            self.t = t
        return np.sum(np.sum(self.buf[:-2].reshape(self.height, 4, self.width, 4), axis=3), axis=1) / 8


class Rings(Effect):

    def __call__(self, t):
        x, y = self.distance_from_centre(dx = math.sin(t * 2.0) * 16.0, dy = math.cos(t * 3.0) * 16.0)
        sc = (math.cos(t * 5.0) * 10.0) + 20.0
        return np.mod(np.sqrt((x**2) + (y**2)[:, np.newaxis])/sc, 1)


class Swirl(Effect):

    def __call__(self, t):
        x, y = self.distance_from_centre()
        dist = (np.sqrt((x**2) + (y**2)[:, np.newaxis]) * (0.5 + (0.2*math.sin(t*0.5)))) + (-t * 5)
        s = np.sin(dist)
        c = np.cos(dist)
        xs = x * c - y[:, np.newaxis] * s
        ys = x * s + y[:, np.newaxis] * c
        return np.mod((np.abs(xs + ys) * 0.05) + (0.1 * t), 1)


class Tunnel(Effect):

    def __init__(self, width, height, nbeams=None):
        super().__init__(width, height)
        self.b = Beams(width, height, nbeams)
        self.z = ZoomRings(width, height)

    def __call__(self, t):
        return (self.z(t) * 0.45) + (self.b(t) * 0.45) + 0.1


class Wind(Effect):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.t = 0
        self.buf = np.random.randint(0, 6, (height, width), dtype=np.uint8) == 0
        self.acc_buf = np.zeros((self.height, self.width), dtype=np.float)

    def __call__(self, t):
        if t - self.t > 0.02:
            self.buf = np.roll(self.buf, 1, axis=1)
            self.buf[:,0] = (np.random.randint(0, 6, (self.height,), dtype=np.uint8) == 0)
            self.acc_buf = np.clip((self.acc_buf - 0.1), 0, 1) + self.buf
            self.t = t
            self.acc_buf = np.clip(self.acc_buf, 0.1, 1.0)
        return self.acc_buf


class Diamonds(Effect):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.buf = np.random.randint(0, 8, (self.height, self.width), dtype=np.uint16)
        self.t = 0

    def __call__(self, t):
        if t - self.t > 0.05:
            self.buf = np.amax(np.stack([
                self.buf,
                np.roll(self.buf, 1, axis=0),
                np.roll(self.buf, -1, axis=0),
                np.roll(self.buf, 1, axis=1),
                np.roll(self.buf, -1, axis=1)
            ]), axis=0)
            self.buf[random.randint(0, self.height-1), random.randint(0, self.width-1)] += 1
            if np.all(self.buf > 256):
                self.buf = self.buf - 256
            self.t = t
        return (self.buf & 0x3) / 3


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

def random_ca(width, height):
    mask = random.choice([Checker, ZoomRings, Beams, Metaballs])(width, height)
    return chromatic_aberration(mask)

def random_mult(width, height):
    grey = random.choice([Swirl, Rings])(width, height)
    colr = random.choice([hue, trippy])
    mask = random.choice([Checker, Tunnel, ZoomRings, Beams, Life, TinyLife, Metaballs, Wind, Diamonds])(width, height)
    return multiply(colr(grey), mask)

def random_invert_mult(width, height):
    # functions are composable in complex ways but on the small screen
    # it mostly ends up looking messy if too much stuff is going on
    grey = random.choice([Swirl])(width, height)
    colr = random.choice([hue, trippy])
    if random.choice([True, False]):
        mask = random.choice([ZoomRings, Beams])(width, height)
        return add(multiply(colr(grey), mask), multiply(colr(shift(grey)), invert(mask)))
    else:
        mask = random.choice([Life, Metaballs])()
        return multiply(colr(grey), invert(mask))

def random_matrix(width, height):
    if random.randint(0,4) == 0:
        return multiply(Matrix(width, height), Roni(width, height))
    else:
        return Matrix(width, height)

def random_simple(width, height):
    grey = random.choice([Swirl, Rings])(width, height)
    colour = random.choice([hue, trippy])
    return colour(grey)

def random_effect(width, height):
    return random.choice([
        random_ca,
        random_mult,
        random_mult,
        random_matrix,
        random_simple
    ])(width, height)

def intro_effect(width, height):
    return multiply(hue(Rings(width, height)), Roni(width, height))