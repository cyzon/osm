from dataclasses import dataclass
from pprint import pprint


@dataclass
class Screenshot:
    size: int
    width: int
    height: int
    data: bytes

@dataclass
class PCLocation:
    cell: int
    x: float
    y: float
    z: float

class CreatedRecord:
    record_type: bytes
    size: int
    flags: int
    form_id: int
    vc_info: int
    data: bytes

    def __init__(self, record_type, size, flags, form_id, vc_info, data):
        self.record_type = record_type
        self.size = size
        self.flags = flags
        self.form_id = form_id
        self.vc_info = vc_info
        self.data = data
        self.fields = []

        match self.record_type:
            case b"SPEL":
                offset = 0

                while offset < self.size:
                    field_type = self.data[offset:offset+4]
                    field_size = int.from_bytes(self.data[offset+4:offset+6], 'little')
                    field_data = self.data[offset+6:offset+6+field_size]

                    record = FieldRecord(field_type, field_size, field_data)
                    self.fields.append(record)
                    
                    # if record.record is None:
                        # print(f"Field type: {field_type}")
                        # print(f"Field size: {field_size}")
                        # print(f"Field data: {field_data}")
                    pprint(record)
                    # print(record.record)

                    offset += 6 + field_size
                
                # print(f"Field type: {field_type}")
                # print(f"Field size: {field_size}")
                # print(f"Field data: {field_data}")
            case _:
                print(f"[E] Unknown change record type: \"{self.record_type}\", skipping")

    def __str__(self):
        return f"CreatedRecord({self.record_type}, {self.size}, {self.flags}, {self.form_id}, {self.vc_info}, {self.data})"
    # TODO: fields: list[FieldRecord]


@dataclass
class FileHeader:
    header: bytes
    major_version: int
    minor_version: int
    exe_time: bytes

@dataclass
class SaveHeader:
    header_version: int
    save_header_size: int
    save_num: int
    pc_name: str
    pc_level: int
    pc_cell_name: str
    game_days: float
    game_ticks: int
    game_time: bytes
    screenshot: Screenshot

@dataclass    
class Globals:
    form_ids_offset: int
    records_num: int
    next_object_id: int
    world_id: int
    world_x: int
    world_y: int
    pc_location: PCLocation
    globals_num: int
    global_vars: dict[int, float]
    tes_class_size: int
    num_death_counts: int
    death_counts: dict[int, int]
    game_time_seconds: int
    processes_size: int
    processes_data: bytes
    spec_event_size: int
    spec_event_data: bytes
    weather_size: int
    weather_data: bytes
    pc_combat_count: int
    created_num: int
    created_records: list[CreatedRecord]
    quick_keys_size: int
    quick_keys_data: list[int]
    reticle_size: int
    reticle_data: bytes
    interface_size: int
    interface_data: bytes
    regions_size: int
    regions_num: int
    regions: dict[int, int]


{
# 6	    FACT	Factions
# 19	APPA	Alchemical Apparatus
# 20	ARMO	Armor
# 21	BOOK	Books
# 22	CLOT	Clothing
# 25	INGR	Ingredients
# 26	LIGH	Lights
# 27	MISC	Misc. Items
# 33	WEAP	Weapons
# 34	AMMO	Arrows
# 35	NPC_	Player and NPC data: attributes, spells, factions, etc.
#               These changes affect all instances of objects.
#               The change record for FormId 0x00000007 contains player character data (see also ACHR).
# 36	CREA	Creature information (rats, horses, hostile creatures.)
#               These changes affect all instances of objects.
# 38	SLGM	Soul gems
# 39	KEYM	Keys
# 40	ALCH	Alchemy (potions)
# 48	CELL	Cells
# 49	REFR	Placed instances of inanimate objects (containers, dropped items, chairs, doors, etc.)
# 50	ACHR	Placed instances of PC (player character) and NPCs (non-player characters).
#               The change record for FormId 0x00000014 (20) contains player character data (see also NPC_).
# 51	ACRE	Placed instances of creatures.
# 58	INFO	Dialog entries.
# 59	QUST	Quest information
# 61	PACK	AI Packages.
#
# Source: https://en.uesp.net/wiki/Oblivion_Mod:Save_File_Format#ChangeRecords
}
change_record_types = {
     6: "FACT", 19: "APPA", 20: "ARMO", 21: "BOOK", 22: "CLOT", 25: "INGR",
    26: "LIGH", 27: "MISC", 33: "WEAP", 34: "AMMO", 35: "NPC_", 36: "CREA",
    38: "SLGM", 39: "KEYM", 40: "ALCH", 48: "CELL", 49: "REFR", 50: "ACHR",
    51: "ACRE", 58: "INFO", 59: "QUST", 61: "PACK",

}
@dataclass
class ChangeRecord:
    form_id: int
    _type: int
    flags: int
    version: int
    data_size: int
    data: bytes

@dataclass
class TemporaryEffects:
    size: int
    data: bytes

@dataclass
class FormIds:
    num: int
    ids: list[int]

@dataclass
class WorldSpaces:
    num: int
    spaces: list[int]

class FieldRecord:
    def __init__(self, type, size, data):
        self._type = type
        self.size = size
        self.data = data
        self.record: FieldRecord

        match self._type:
            case b"EFID":
                self.record = EFID(self.size, self.data)
            case b"FULL":
                self.name = self.data[:self.size].decode("utf-8")
                self.record = FULL(self.size, self.data)
            case _:
                print(f"[E] Unknown field record type: {self._type}")
                self.record = None

    def __str__(self):
        return f"FieldRecord(_type: {self._type}, size: {self.size}, " \
                           f"data: u8[{len(self.data)}], record: {self.record})"

    def __repr__(self):
        return self.__str__()

# Contains the form ID for a magic effect. (MGEF)
# https://en.uesp.net/wiki/Skyrim_Mod:Mod_File_Format/MGEF
class EFID:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.form_id = int.from_bytes(self.data[:4], "little")

    def __str__(self):
        return f"EFID(form_id: {hex(self.form_id)}, size: {self.size}, data: u8[{len(self.data)}])"

    def __repr__(self):
        return self.__str__()

# Full in-game name of an object.
# The data field contains a null-terminated string.
class FULL:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.name = self.data[:self.size].decode("utf-8")

    def __str__(self):
        return f"FULL(name: \"{self.name}\", size: {self.size}, data: u8[{len(self.data)}])"

    def __repr__(self):
        return self.__str__()