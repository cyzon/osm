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
        records_num = self.globals.records_num
        self.change_records: list[ChangeRecord] = self.reader.read_change_records(records_num)
        self.temporary_effects = self.reader.read_temporary_effects()
        self.form_ids = self.reader.read_form_ids()
        self.worldspaces = self.reader.read_world_spaces()


    def __del__(self):
        del self.reader

    def __str__(self):
        return f"OblivionSave({self.reader.filename})"

    def __repr__(self):
        return self.__str__()

