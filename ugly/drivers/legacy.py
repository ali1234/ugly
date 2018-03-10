# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

from importlib import import_module

from ugly.buffer import Drawable
from ugly.drivers.base import Driver

class Legacy(Driver, Drawable):
    """
    Legacy driver. Passes through calls to some other driver.
    Does not need its own framebuffer as the legacy driver has one.
    """
    # TODO: may need multiple versions of this
    # as the legacy drivers are all slightly different.

    def __init__(self, legacy, depth):
        self.__legacy = import_module(legacy)
        super().__init__(self.__legacy._buf, depth, legacy)

    def __enter__(self):
        return super().__enter__()

    def show(self):
        self.__legacy.show()
        super().show()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__legacy.off()
        super().__exit__(exc_type, exc_val, exc_tb)
