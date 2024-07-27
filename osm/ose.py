import os

from pprint import pprint

from oblivion_save import *
# from helpers import FileReader, PCLocation, Record, ChangeRecord



def main():
    inf = OblivionSaveReader("C:\\Users\\Czyzx\\Documents\\My Games\\Oblivion\\Saves\\autosave.ess")

    header = inf.read_bytes(12)
    major_version = inf.read_u8()
    minor_version = inf.read_u8()
    filetime = inf.read_bytes(16)
    header_version = inf.read_u32()
    save_header_size = inf.read_u32()
    save_num = inf.read_u32()
    pc_name = inf.read_bzstr()
    pc_level = inf.read_u16()
    pc_cell_name = inf.read_bzstr()
    game_days = inf.read_float()
    game_ticks = inf.read_u32()
    game_time = inf.read_bytes(16)
    screenshot = inf.read_screenshot()
    plugin_num = inf.read_u8()
    plugin_names = [inf.read_bstr() for i in range(plugin_num)]
    form_ids_offset = inf.read_u32()
    records_num = inf.read_u32()
    next_object_id = inf.read_u32()
    world_id = inf.read_u32()
    world_x = inf.read_u32()
    world_y = inf.read_u32()
    pc_location = PCLocation(
        inf.read_u32(),      # FormID of cell
        inf.read_float(),    # pc_x
        inf.read_float(),    # pc_y
        inf.read_float()     # pc_z
    )
    globals_num = inf.read_u16()
    global_vars = {
        inf.read_u32(): inf.read_float()
        for _ in range(globals_num)
    }
    tes_class_size = inf.read_u16() # num_death_counts * 6 + 8
    # 
    num_death_counts = inf.read_u32()
    death_counts = {    # {actor_iref: death_count}
        inf.read_u32(): inf.read_u16()
        for _ in range(num_death_counts)
    }
    gametime_seconds = inf.read_float()
    # Processes data, dunno what any of this represents.
    processes_size = inf.read_u16()
    processes_data = inf.read_bytes(processes_size)
    # Spectator event data.
    spec_event_size = inf.read_u16()
    spec_event_data = inf.read_bytes(spec_event_size)
    # Weather data, not sure what's in here yet either.
    weather_size = inf.read_u16()
    weather_data = inf.read_bytes(weather_size)
    # Number of actors in combat with the player.
    pc_combat_count = inf.read_u32()
    # Created data, this includes spells, enchantments and potions created
    #  in-game.
    # Number of records.
    created_num: int = inf.read_u32()
    created_records: list[Record] = []

    for _ in range(created_num):
        record_type = inf.read_bytes(4)
        record_size = inf.read_u32()
        record_flags = inf.read_u32()
        record_form_id = inf.read_u32()
        record_vc_info = inf.read_u32()
        record_data = inf.read_bytes(record_size)

        record = Record(
            record_type,
            record_size,
            record_flags,
            record_form_id,
            record_vc_info,
            record_data
        )

        created_records.append(record)

    
    saved_pos = inf.position
    quick_keys_size = inf.read_u16()
    quick_keys_data = []
    #   scan the quick_keys array.  quick_keys_size is the number of bytes in the array.  If flag is 1
    # the quickkey is set and the next 4 bytes are an iref for the setting.
    while inf.position < saved_pos + quick_keys_size:
        flag = inf.read_u8()
        quick_keys_data.append(inf.read_u32() if flag == 1 else 0)

    reticle_size = inf.read_u16()
    reticle_data = inf.read_bytes(reticle_size)
    interface_size = inf.read_u16()
    interface_data = inf.read_bytes(interface_size)
    
    regions_size = inf.read_u16()
    regions_num = inf.read_u16()
    # (iref, unknown_6)
    regions_data = [(inf.read_u32(), inf.read_u32()) for _ in range(regions_num)]

    change_records: list[ChangeRecord] = []

    for _ in range(records_num):
        cr_form_id = inf.read_u32()
        cr_type = inf.read_u8()
        cr_flags = inf.read_u32()
        cr_version = inf.read_u8()
        cr_data_size = inf.read_u16()
        cr_data = inf.read_bytes(cr_data_size)

        change_records.append(
            ChangeRecord(cr_form_id, cr_type, cr_flags, cr_version, cr_data_size, cr_data)
        )


    temporary_effects_size = inf.read_u32()
    temporary_effects_data = inf.read_bytes(temporary_effects_size)
   
    form_ids_num = inf.read_u32()
    form_ids = [inf.read_u32() for _ in range(form_ids_num)]

    world_spaces_num = inf.read_u32()
    world_spaces = [inf.read_u32() for _ in range(world_spaces_num)]
   
    pprint(f"file position: {inf.file.tell()}")
    pprint(f"file size:  {os.path.getsize(inf.filename)}")


    pprint(f"header: {header}")
    pprint(f"major_version: {major_version}")
    pprint(f"minor_version: {minor_version}")
    pprint(f"filetime: {filetime}")
    pprint(f"header_version: {header_version}")
    pprint(f"save_header_size: {save_header_size}")
    pprint(f"save_num: {save_num}")
    pprint(f"pc_name: {pc_name}")
    pprint(f"pc_level: {pc_level}")
    pprint(f"pc_cell_name: {pc_cell_name}")
    pprint(f"game_days: {game_days}")
    pprint(f"game_ticks: {game_ticks}")
    pprint(f"game_time: {game_time}")
    print("screenshot {")
    pprint(f"   size: {screenshot.size}")
    pprint(f"   width: {screenshot.width}")
    pprint(f"   height: {screenshot.height}")
    pprint(f"plugin_num: {plugin_num}")
    pprint(f"plugin_names: {plugin_names}")
    pprint(f"form_ids_offset: {form_ids_offset}")
    pprint(f"records_num: {records_num}")
    pprint(f"next_object_id: {next_object_id}")
    pprint(f"world_id: {world_id}")
    pprint(f"world_x: {world_x}")
    pprint(f"world_y: {world_y}")
    print(f"pc_location {{\n\t"
          f"cell_id: {pc_location.cell},\n\t"
          f"x: {pc_location.x},\n\t"
          f"y: {pc_location.y},\n\t"
          f"z: {pc_location.z}\n}}"
    )

    pprint(f"globals_num: {globals_num}")
    # for gv in global_vars:
    #     pprint(f"{{iref: {gv.iref}, value: {gv.value}}}")

    pprint(f"num_death_counts: {num_death_counts}")
    # for dc in death_counts:
    #     pprint(f"{{actor: {dc.actor}, count: {dc.count}}}")

    pprint(f"gametime_seconds: {gametime_seconds}")
    
    pprint(f"processes_size: {processes_size}")
    # pprint(f"processes_data: {processes_data}")

    pprint(f"spec_event_size: {spec_event_size}")
    # pprint(f"spec_event_data: {spec_event_data}")

    pprint(f"weather_size: {weather_size}")
    # pprint(f"weather_data: {weather_data}")

    pprint(f"pc_combat_count: {pc_combat_count}")
    pprint(f"created_num: {created_num}")

    for record in created_records:
        print(f"record_type: {record.record_type}")
        print(f"record_size: {record.size}")
        print(f"record_flags: {record.flags}")
        print(f"record_form_id: {record.form_id}")
        print(f"record_vc_info: {record.vc_info}")
        print(f"record_data: {record.data}")
    
    pprint(f"quick_keys_size: {quick_keys_size}")
    pprint(f"quick_keys_data: {quick_keys_data}")
    pprint(f"reticle_size: {reticle_size}")
    pprint(f"reticle_data: {reticle_data}")
    pprint(f"interface_size: {interface_size}")
    pprint(f"interface_data: {interface_data}")
    pprint(f"regions_size: {regions_size}")
    pprint(f"regions_num: {regions_num}")
    # pprint(f"regions_data: {regions_data}")
    
    change_records_sorted = sorted(change_records, key=lambda r: r._type)
    test = [change_record_types[r._type] for r in change_records_sorted]
    record_types = set(test)
    record_counts = {_type: test.count(_type) for _type in record_types}

    pprint(record_counts)

    # for r in change_records_sorted:
    #     print(change_record_types[r._type], r.form_id, r._type, hex(r.flags), r.version, r.data_size)

    pprint(f"temporary_effects_size: {temporary_effects_size}")
    # pprint(f"temporary_effects_data: {temporary_effects_data}")


if __name__ == "__main__":
    main()
