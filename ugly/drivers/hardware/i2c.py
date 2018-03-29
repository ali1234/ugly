# * Copyright 2018 Alistair Buxton <a.j.buxton@gmail.com>
# *
# * License: This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License as published
# * by the Free Software Foundation; either version 3 of the License, or (at
# * your option) any later version. This program is distributed in the hope
# * that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.

# Helpers for I2C-based drivers.


class Register(object):

    def __init__(self, offset):
        self._offset = offset

    def retry(self, f, *args):
        max_retries = 3
        for i in range(1, max_retries+1):
            try:
                return f(*args)
            except IOError:
                if i == max_retries:
                    raise
                else:
                    continue

    def __set__(self, obj, value):
        if type(value) is list:
            for i in range(0, len(value), 32):
                self.retry(obj._bus.write_i2c_block_data, obj._address, self._offset+i, value[i:i+32])
        else:
            self.retry(obj._bus.write_byte_data, obj._address, self._offset, value)


class BankedRegister(Register):

    def __init__(self, bank_offset, bank, offset):
        super().__init__(offset)
        self._bank = bank
        self._bank_offset = bank_offset

    def __set__(self, obj, value):
        self.retry(obj._bus.write_byte_data, obj._address, self._bank_offset, self._bank)
        return super().__set__(obj, value)


class Command(Register):

    def __init__(self, offset, mask):
        super().__init__(offset)
        self._mask = mask

    def __set__(self, obj, value):
        self.retry(obj._bus.write_byte, obj._address, self._offset | (value&self._mask))
