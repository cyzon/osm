import struct

from oblivion_types import *


class OblivionSaveReader:
    def __init__(self, filename):
        self.filename = filename
        self.position = 0
        self.file = open(filename, "rb")

    def __del__(self):
        self.file.close()

    

    def read_formatted(self, format, length, offset):
        if offset:
            self.file.seek(offset)
        else:
            self.file.seek(self.position)
        
        raw = self.file.read(length)
        self.position += length

        return struct.unpack(format, raw)
    
    def read_bytes(self, length, offset=None):
        if offset:
            self.file.seek(offset)
            self.position = offset
        else:
            self.file.seek(self.position)

        self.position += length
        return self.file.read(length)
    
    def read_char(self, offset=None): return self.read_formatted("c", 1, offset)[0]
    def read_i8(self, offset=None): return int(self.read_formatted("b", 1, offset)[0])
    def read_u8(self, offset=None): return int(self.read_formatted("B", 1, offset)[0])
    def read_i16(self, offset=None): return int(self.read_formatted("h", 2, offset)[0])
    def read_u16(self, offset=None): return int(self.read_formatted("H", 2, offset)[0])
    def read_i32(self, offset=None): return int(self.read_formatted("i", 4, offset)[0])
    def read_u32(self, offset=None): return int(self.read_formatted("I", 4, offset)[0])
    def read_i64(self, offset=None): return int(self.read_formatted("q", 8, offset)[0])
    def read_u64(self, offset=None): return int(self.read_formatted("Q", 8, offset)[0])
    def read_float(self, offset=None): return float(self.read_formatted("f", 4, offset)[0])
    def read_double(self, offset=None): return float(self.read_formatted("d", 8, offset)[0])
    def read_bzstr(self, offset=None): return self.read_bytes(self.read_u8())[:-1]
    def read_bstr(self, offset=None):  return self.read_bytes(self.read_u8())

    def read_zstr(self):
        chars = b""        
        c = self.read_char()

        while c != b'\x00':
            chars += c
            c = self.read_char()

        self.position += 1

        return chars
    
    def read_screenshot(self, offset=None):
        size = self.read_u32()
        width = self.read_u32()
        height = self.read_u32()
        data = self.read_bytes(3*width*height)

        return Screenshot(size, width, height, data)
        
    # TODO: create class for timestamp and read it properly
    def read_timestamp(self, offset=None): return self.read_formatted("s", 16, pos)
