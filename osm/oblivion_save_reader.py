import struct

from oblivion_types import *

class OblivionSaveReader:
    def __init__(self, filename):
        self.filename = filename
        self.position = 0
        self.file = open(filename, "rb")

    def __del__(self):
        self.file.close()

    def read_file_header(self):
        header = self.read_bytes(12)
        major_version = self.read_u8()
        minor_version = self.read_u8()
        exe_time = self.read_bytes(16)

        return FileHeader(header, major_version, minor_version, exe_time)

    def read_save_header(self):
        header_version = self.read_u32()
        save_header_size = self.read_u32()
        save_num = self.read_u32()
        pc_name = self.read_bzstr()
        pc_level = self.read_u16()
        pc_cell_name = self.read_bzstr()
        game_days = self.read_float()
        game_ticks = self.read_u32()
        game_time = self.read_bytes(16)
        screenshot = self.read_screenshot()

        return SaveHeader(
            header_version,
            save_header_size,
            save_num,
            pc_name,
            pc_level,
            pc_cell_name,
            game_days,
            game_ticks,
            game_time,
            screenshot
        )

    def read_plugins(self):
        plugin_num = self.read_u8()
        plugin_names = [self.read_bstr() for _ in range(plugin_num)]

        return plugin_names

    def read_globals(self):
        form_ids_offset = self.read_u32()
        records_num = self.read_u32()
        next_object_id = self.read_u32()
        world_id = self.read_u32()
        world_x = self.read_u32()
        world_y = self.read_u32()
        pc_location = PCLocation(
            self.read_u32(),
            self.read_float(),
            self.read_float(),
            self.read_float()
        )
        globals_num = self.read_u16()
        global_vars = {
            self.read_u32(): self.read_float()
            for _ in range(globals_num)
        }
        tes_class_size = self.read_u16()
        num_death_counts = self.read_u32()
        death_counts = {
            self.read_u32(): self.read_u16()
            for _ in range(num_death_counts)
        }
        # Number of second spent in-game with no menus open.
        gametime_seconds = self.read_float()
        processes_size = self.read_u16()
        processes_data = self.read_bytes(processes_size)
        spec_event_size = self.read_u16()
        spec_event_data = self.read_bytes(spec_event_size)
        weather_size = self.read_u16()
        weather_data = self.read_bytes(weather_size)
        pc_combat_count = self.read_u32()
        # Created data, this includes spells, enchantments and potions created in-game.
        # The format is the same as the mod file record format.
        created_num = self.read_u32()
        created_records: list[CreatedRecord] = []


        for _ in range(created_num):
            record_type = self.read_bytes(4)
            record_size = self.read_u32()
            flags = self.read_u32()
            form_id = self.read_u32()
            vc_info = self.read_u32()
            data = self.read_bytes(record_size)

            record = CreatedRecord(
                record_type, record_size, flags, form_id, vc_info, data
            )

            created_records.append(record)

        saved_pos = self.position
        #   Quick Keys settings. The size of individual data records can be 1 or 5 bytes, depending
        # upon the value of "flag" in each record.  If flag is 0 the key is not set, if flag is 1
        # the key is set and an iref follows.
        quick_keys_size = self.read_u16()
        quick_keys_data = []

        while self.position < saved_pos + quick_keys_size:
            flag = self.read_u8()
            
            if flag == 0:
                quick_keys_data.append(0)
            else:
                quick_keys_data.append(1)
                quick_keys_data.append(self.read_u32())

        # Reticle data, not sure what this is yet.
        reticle_size = self.read_u16()
        reticle_data = self.read_bytes(reticle_size)
        # Interface stuff, not sure what this is yet.
        interface_size = self.read_u16()
        interface_data = self.read_bytes(interface_size)
        # Information about regions.
        regions_save = self.read_u16()
        regions_num = self.read_u16()
        regions_data = [(self.read_u32(), self.read_u32()) for _ in range(regions_num)]

        return Globals(
            form_ids_offset, records_num, next_object_id, world_id, world_x, world_y, pc_location,
            globals_num, global_vars, tes_class_size, num_death_counts, death_counts, gametime_seconds,
            processes_size, processes_data, spec_event_size, spec_event_data, weather_size, weather_data,
            pc_combat_count, created_num, created_records, quick_keys_size, quick_keys_data, reticle_size,
            reticle_data, interface_size, interface_data, regions_save, regions_num, regions_data
        )

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
