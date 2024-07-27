

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

change_record_types = {
     6: "FACT", 19: "APPA", 20: "ARMO", 21: "BOOK", 22: "CLOT", 25: "INGR",
    26: "LIGH", 27: "MISC", 33: "WEAP", 34: "AMMO", 35: "NPC_", 36: "CREA",
    38: "SLGM", 39: "KEYM", 40: "ALCH", 48: "CELL", 49: "REFR", 50: "ACHR",
    51: "ACRE", 58: "INFO", 59: "QUST", 61: "PACK",

}


class Screenshot:
    def __init__(self, size, width, height, data) -> None:
        self.size = size
        self.width = width
        self.height = height
        self.data = data

class PCLocation:
    def __init__(self, cell, x, y, z):
        self.cell = cell
        self.x = x
        self.y = y
        self.z = z

class Record:
    def __init__(self, record_type, size, flags, form_id, vc_info, data):
        self.record_type = record_type
        self.size = size
        self.flags = flags
        self.form_id = form_id
        self.vc_info = vc_info
        self.data = data
        # TODO: add a list of field records
        # self.fields = fields

class ChangeRecord:
    def __init__(self, form_id, _type, flags, version, data_size, data):
        self.form_id = form_id
        self._type = _type
        self.flags = flags
        self.version = version
        self.data_size = data_size
        self.data = data
