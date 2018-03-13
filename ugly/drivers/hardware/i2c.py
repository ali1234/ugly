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

    def __get__(self, obj, objtype):
        return self.retry(obj._bus.readfrom_mem, obj._address, self._offset, 1)[0]

    def __set__(self, obj, value):
        if type(value) is list:
            for i in range(0, len(value), 32):
                self.retry(obj._bus.write_i2c_block_data, obj._address, self._offset+i, value[i:i+32])
        else:
            self.retry(obj._bus.write_i2c_block_data, obj._address, self._offset, [value])


class BankedRegister(Register):

    def __init__(self, bank_offset, bank, offset):
        super().__init__(offset)
        self._bank = bank
        self._bank_offset = bank_offset

    def __get__(self, obj, objtype):
        self.retry(obj._bus.write_i2c_block_data, obj._address, self._bank_offset, [self._bank])
        return super().__get__(obj, objtype)

    def __set__(self, obj, value):
        self.retry(obj._bus.write_i2c_block_data, obj._address, self._bank_offset, [self._bank])
        return super().__set__(obj, value)
