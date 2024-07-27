import struct

from oblivion_types import *
from oblivion_save_reader import OblivionSaveReader


class OblivionSave:
    def __init__(self, filename):
        self.reader = OblivionSaveReader(filename)

        self.file_header: FileHeader = self.reader.read_file_header()
        self.save_header: SaveHeader = self.reader.read_save_header()
        self.plugins: list[bytes] = self.reader.read_plugins()
        self.globals: Globals = self.reader.read_globals()

    def __del__(self):
        del self.reader

    def __str__(self):
        return f"OblivionSave({self.reader.filename})"

    def __repr__(self):
        return self.__str__()

