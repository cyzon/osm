from dataclasses import dataclass
from pprint import pprint
import struct


@dataclass
class Screenshot:
    size: int
    width: int
    height: int
    data: bytes

    def __str__(self):
        return f"Screenshot(size: {self.size}, width: {self.width}, height: {self.height}, " \
               f"data: u8[{len(self.data)}])"
    
    def __repr__(self):
        return self.__str__()

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
        
        # print(self.record_type)

        offset = 0

        while offset < self.size:
            field_type = self.data[offset:offset+4]
            field_size = int.from_bytes(self.data[offset+4:offset+6], 'little')
            field_data = self.data[offset+6:offset+6+field_size]

            record = FieldRecord(field_type, field_size, field_data)
            self.fields.append(record)
            
            offset += 6 + field_size

    def __str__(self, depth=0):
        ret = "    "*depth + "CreateRecord {\n" + \
              "    "*(depth+1)+ f"record_type: {self.record_type},\n" + \
              "    "*(depth+1)+ f"size: {self.size},\n" + \
              "    "*(depth+1)+ f"flags: {self.flags},\n" + \
              "    "*(depth+1)+ f"form_id: {hex(self.form_id).upper()},\n" + \
              "    "*(depth+1)+ f"vc_info: {self.vc_info},\n" + \
              "    "*(depth+1)+  "fields: [\n"
        
        for field in self.fields:
            ret += field.__str__(depth+2)
            ret += "]" + \
                   "    "*depth + "},\n"
        
        return ret
    
    def __repr__(self):
        return self.__str__()

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
    regions_data: list[tuple[int, int]] 


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
cr_type_names = {
     6: "FACT", 19: "APPA", 20: "ARMO", 21: "BOOK", 22: "CLOT", 25: "INGR",
    26: "LIGH", 27: "MISC", 33: "WEAP", 34: "AMMO", 35: "NPC_", 36: "CREA",
    38: "SLGM", 39: "KEYM", 40: "ALCH", 48: "CELL", 49: "REFR", 50: "ACHR",
    51: "ACRE", 58: "INFO", 59: "QUST", 61: "PACK",

}

class ChangeRecord:
    form_id: int
    _type: int
    cr_flags: int
    version: int
    data_size: int
    data: bytes

    def __init__(self, form_id, cr_type, cr_flags, version, data_size, data):
        self.cr_form_id = form_id
        self.cr_type = cr_type
        self.cr_flags = cr_flags
        self.version = version
        self.data_size = data_size
        self.data = data
        self.subrecords = []

        self.has_form_flags = bool(self.cr_flags & 0x00000001)

        # print(cr_type_names[self._type])


        match self.cr_type:
            case 6:
                print("FACT")
                self.subrecords.append(FACT(self.cr_flags, self.data_size, self.data))
                print(self.subrecords[-1])
            case 19:
                # print("APPA")
                pass
            case 20:
                # print("ARMO")
                pass
            case 21:
                # print("BOOK")
                self.subrecords.append(BOOK(self.cr_flags, self.data_size, self.data))
                # print(self.subrecords[-1])
            case 22:
                # print("CLOT")
                pass
            case 25:
                # print("INGR")
                pass
            case 26:
                # print("LIGH")
                pass
            case 27:
                # print("MISC")
                pass
            case 33:
                # print("WEAP")
                pass
            case 34:
                # print("AMMO")
                pass
            case 35:
                # print("NPC_")
                pass
            case 36:
                # print("CREA")
                pass
            case 38:
                # print("SLGM")
                pass
            case 39:
                # print("KEYM")
                pass
            case 40:
                # print("ALCH")
                pass
            case 48:
                # print("CELL")
                pass
            case 49:
                # print("REFR")
                pass
            case 50:
                # print("ACHR")
                pass
            case 51:
                # print("ACRE")
                pass
            case 58:
                # print("INFO")
                pass
            case 59:
                # print("QUST")
                pass
            case 61:
                # print("PACK")
                pass
            case _:
                print(f"[E] Unknown change record type: {self.cr_type}")

#   The Form Flags subrecord is present when bit 0 (0x00000001) is set in any 
# change record's overall Flags. Its length is a constant 4 bytes.
# The Value subrecord is present when bit 3 (0x00000008) is set in any change
# record's overall Flags. Its length is a constant 4 bytes.
# The Teaches subrecord is present when bit 2 (0x00000004) is set in any change
# record's overall Flags. Its length is a constant 1 byte. A value of 255
# indicates that the book teaches has been read and teaches no skills.
class BOOK:
    def __init__(self, cr_flags, size, data):
        self.cr_flags = cr_flags
        self.size = size
        self.data = data
        # optional fields
        self.form_flags = None
        self.value = None
        self.teaches = None

        offset = 0

        if cr_flags & 0x00000001:
            self.form_flags = int.from_bytes(self.data[:4], "little")
            offset += 4
        if cr_flags & 0x00000008:
            self.value = int.from_bytes(self.data[offset:offset+4], "little")
            offset += 4
        if cr_flags & 0x00000004:
            self.teaches = int.from_bytes(self.data[offset:offset+1], "little")
    
    def __str__(self, depth=0):
        return "   "*depth + "BOOK {\n" + \
               "   "*(depth+1) + f"cr_flags: {self.cr_flags},\n" + \
               "   "*(depth+1) + f"form_flags: {self.form_flags},\n" + \
               "   "*(depth+1) + f"value: {self.value},\n" + \
               "   "*(depth+1) + f"teaches: {self.teaches},\n" + \
               "   "*(depth) + "}"
    
    def __repr__(self):
        return self.__str__()
    
class FACT:
    def __init__(self, cr_flags, size, data):
        self.cr_flags = cr_flags
        self.size = size
        self.data = data
        # optional fields
        self.reactions_num = None
        self.reactions = None
        self.flags = None

        offset = 0

        if cr_flags & 0x00000008:
            self.reactions_num = int.from_bytes(self.data[:2], "little")
            self.reactions = []

            for _ in range(self.reactions_num):
                self.reactions.append(
                    (int.from_bytes(self.data[offset:offset+4], "little"),
                    int.from_bytes(self.data[offset+4:offset+8], "little")))
                offset += 8
                
            offset += 2

        if cr_flags & 0x00000004:
            self.flags = int.from_bytes(self.data[offset:offset+1], "little")


    def __str__(self, depth=0):
        ret =  "   "*depth + "FACT {\n" + \
               "   "*(depth+1) + f"cr_flags: {self.cr_flags},\n" + \
               "   "*(depth+1) + f"reactions_num: {self.reactions_num},\n"
        
        for reaction in self.reactions:
            ret += "   "*(depth+2) + f"reaction: ({reaction[0]}, {reaction[1]}),\n"

        ret += "   "*(depth+1) + f"flags: {self.flags},\n" + \
               "   "*(depth) + "}"
        
        return ret
    
    def __repr__(self):
        return self.__str__()



class SubRecord:
    def __init__(self, rec_type, size, flags, form_id, version, data):
        self.form_id = form_id
        self.rec_type = rec_type
        self.flags = flags
        self.version = version
        self.data_size = size
        self.data = data
        self.record = None

        # Is the data compressed?
        if self.flags & 0x00040000:
            print(f"[E] Compressed data: {self.rec_type}: ")
            self.record = None
        elif self.rec_type not in cr_type_names:
            print(f"[E] Unknown subrecord type: {self.rec_type}: ")
            self.record = None

        # match self.rec_type:
        #     case b"ACHR":
        #         print("ACHR")
        #     case _:
        #         # print(f"[E] Unknown subrecord type: {self.rec_type}: ")
        #         self.record = None
        
        # breakpoint()

        

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
        self.record = None

        match self._type:
            case b"ANAM":
                self.record = ANAM(self.size, self.data)
            case b"DATA":
                self.record = DATA(self.size, self.data)
            case b"EFID":
                self.record = EFID(self.size, self.data)
            case b"EFIT":
                self.record = EFIT(self.size, self.data)
            case b"ENAM":
                self.record = ENAM(self.size, self.data)
            case b"ENIT":
                self.record = ENIT(self.size, self.data)
            case b"FULL":
                self.record = FULL(self.size, self.data)
            case b"ICON":
                self.record = ICON(self.size, self.data)
            case b"MODB":
                self.record = MODB(self.size, self.data)
            case b"MODL":
                self.record = MODL(self.size, self.data)
            case b"SPIT":
                self.record = SPIT(self.size, self.data)
            case _:
                print(f"[E] Unknown field record type: {self._type}")
                self.record = None

    def __str__(self, depth=0):
        return "   "*depth + "FieldRecord {\n" + \
               "   "*(depth+1) + f"type: {self._type},\n" + \
               "   "*(depth+1) + f"size: {self.size},\n" + \
               self.record.__str__(depth=depth+1)

    def __repr__(self):
        return self.__str__()

class ANAM:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.enchantment_points = int.from_bytes(self.data[:4], "little")
    
    def __str__(self, depth=0):
        return "   "*depth + f"ANAM(enchantment_points: {self.enchantment_points}),\n"
    
    def __repr__(self):
        return self.__str__()

class DATA:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.type = int.from_bytes(self.data[:4], "little")
        self.speed = struct.unpack("f", self.data[4:8])[0]
        self.reach = struct.unpack("f", self.data[8:12])[0]
        self.flags = int.from_bytes(self.data[12:16], "little")
        self.value = int.from_bytes(self.data[16:20], "little")
        self.health = int.from_bytes(self.data[20:24], "little")
        self.weight = struct.unpack("f", self.data[24:28])[0]
        self.damage = int.from_bytes(self.data[28:30], "little")

    def __str__(self, depth=0):
        return "   "*depth + "DATA {\n" + \
               "   "*(depth+1) + f"type: {hex(self.type)},\n" + \
               "   "*(depth+1) + f"speed: {self.speed},\n" + \
               "   "*(depth+1) + f"reach: {self.reach},\n" + \
               "   "*(depth+1) + f"flags: {bin(self.flags)},\n" + \
               "   "*(depth+1) + f"value: {self.value},\n" + \
               "   "*(depth+1) + f"health: {self.health},\n" + \
               "   "*(depth+1) + f"weight: {self.weight},\n" + \
               "   "*(depth+1) + f"damage: {self.damage},\n"
    
    
    def __repr__(self):
        return self.__str__()

# Contains the form ID for a magic effect. (MGEF)
# https://en.uesp.net/wiki/Skyrim_Mod:Mod_File_Format/MGEF
class EFID:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.form_id = int.from_bytes(self.data[:4], "little")

    def __str__(self, depth=0):
        return "   "*depth + f"EFID(form_id: {hex(self.form_id).upper()})," \

    def __repr__(self):
        return self.__str__()

# Contains the effect data for a magic effect.
# https://en.uesp.net/wiki/Oblivion_Mod:Mod_File_Format/ENCH#EFIT_Subrecord
class EFIT:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.effect_id = int.from_bytes(self.data[:4], "little")
        self.magnitude = int.from_bytes(self.data[4:8], "little")
        self.area = int.from_bytes(self.data[8:12], "little")
        self.duration = int.from_bytes(self.data[12:16], "little")
        self._type = int.from_bytes(self.data[16:20], "little")
        self.actor_value = int.from_bytes(self.data[20:24], "little")

    def __str__(self, depth=0):
        return "   "*depth + "EFIT {\n" + \
                "   "*(depth+1) + f"effect_id: {hex(self.effect_id)},\n" + \
                "   "*(depth+1) + f"magnitude: {self.magnitude},\n" + \
                "   "*(depth+1) + f"area: {self.area},\n" + \
                "   "*(depth+1) + f"duration: {self.duration},\n" + \
                "   "*(depth+1) + f"type: {hex(self._type)},\n" + \
                "   "*(depth+1) + f"actor_value: {hex(self.actor_value)},"

    def __repr__(self):
        return self.__str__()

class ENAM:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.enchantment_form_id = int.from_bytes(self.data[:4], "little")

    def __str__(self, depth=0):
        return "   "*depth + f"ENAM(enchantment_form_id: {hex(self.enchantment_form_id).upper()}),"
    
    def __repr__(self):
        return self.__str__()

class ENIT:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.type = int.from_bytes(self.data[:4], "little")
        self.charge_amount = int.from_bytes(self.data[4:8], "little")
        self.enchantment_cost = int.from_bytes(self.data[8:12], "little")
        self.flags = int.from_bytes(self.data[12:16], "little")

    def __str__(self, depth=0):
        return "   "*depth + "ENIT {\n" + \
               "   "*(depth+1) + f"type: {hex(self.type)},\n" + \
               "   "*(depth+1) + f"charge_amount: {self.charge_amount},\n" + \
               "   "*(depth+1) + f"enchantment_cost: {self.enchantment_cost},\n" + \
               "   "*(depth+1) + f"flags: {bin(self.flags)},"
    
    def __repr__(self):
        return self.__str__()

# Full in-game name of an object.
# The data field contains a null-terminated string.
class FULL:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.name = self.data[:self.size].decode("utf-8")

    def __str__(self, depth=0):
        return "   "*depth + f"FULL(name: \"{self.name}\"),"

    def __repr__(self):
        return self.__str__()
    
class ICON:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.filename = self.data[:self.size].decode("utf-8")

    def __str__(self, depth=0):
        return "   "*depth + "ICON {\n" + \
               "   "*(depth+1) + f"filename: \"{self.filename}\","
    
    
    def __repr__(self):
        return self.__str__()

class MODB:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.data = int.from_bytes(self.data[:4], "little")

    def __str__(self, depth=0):
        return "   "*depth + "MODB(data: {self.data}),"
      
    def __repr__(self):
        return self.__str__()

class MODL:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.filename = self.data[:self.size].decode("utf-8")
    
    def __str__(self, depth=0):
        return "   "*depth + "MODL {\n" + \
               "   "*(depth+1) + f"filename: \"{self.filename}\","
        
    def __repr__(self):
        return self.__str__()

class SCIT:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self.form_id = int.from_bytes(self.data[:4], "little")
        self.school = int.from_bytes(self.data[4:8], "little")
        self.visual_effect = int.from_bytes(self.data[8:12], "little")
        self.flags = bin(int.from_bytes(self.data[12:16], "little"))

    def __str__(self, depth=0):
        return "   "*depth + "SCIT {\n" + \
               "   "*(depth+1) + f"form_id: {hex(self.form_id)},\n" + \
               "   "*(depth+1) + f"school: {hex(self.school)},\n" + \
               "   "*(depth+1) + f"visual_effect: {hex(self.visual_effect)},\n" + \
               "   "*(depth+1) + f"flags: {bin(self.flags)},"
    
    def __repr__(self):
        return self.__str__()

class SPIT:
    def __init__(self, size, data):
        self.size = size
        self.data = data

        self._type = int.from_bytes(self.data[:4], "little")
        self.spell_cost = int.from_bytes(self.data[4:8], "little")
        self.spell_level = int.from_bytes(self.data[8:12], "little")
        self.flags = int.from_bytes(self.data[12:16], "little")
    
    def __str__(self, depth=0):
        return "   "*depth + "SPIT {\n" + \
               "   "*(depth+1) + f"type: {hex(self._type)},\n" + \
               "   "*(depth+1) + f"spell_cost: {self.spell_cost},\n" + \
               "   "*(depth+1) + f"spell_level: {self.spell_level},\n" + \
               "   "*(depth+1) + f"flags: {bin(self.flags)},"
    
    def __repr__(self):
        return self.__str__()
    
