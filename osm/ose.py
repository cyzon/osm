import os

from pprint import pprint

from oblivion_save import *
from utils import chunks


def text_dump(save: OblivionSave):
    pprint(save.file_header)
    pprint(save.save_header)
    pprint(save.plugins)
    pprint(f"save.globals [")
    pprint({"form_ids_offset": save.globals.form_ids_offset})
    pprint({"records_num": save.globals.records_num})
    pprint({"next_object_id": save.globals.next_object_id})
    pprint({"world_id": save.globals.world_id})
    pprint({"world_x": save.globals.world_x})
    pprint({"world_y": save.globals.world_y})
    pprint({"pc_location": save.globals.pc_location})
    pprint({"globals_num": save.globals.globals_num})
    # pprint({"global_vars": save.globals.global_vars})
    pprint({"tes_class_size": save.globals.tes_class_size})
    pprint({"num_death_counts": save.globals.num_death_counts})
    
    print("death_counts: {")
    items = [(k, v) for k, v in save.globals.death_counts.items()]
    for chunk in chunks(items, 8):
        print(chunk)

    pprint({"game_time_seconds": save.globals.game_time_seconds})
    pprint({"processes_size": save.globals.processes_size})
    pprint(f"processes_data: u8[{len(save.globals.processes_data)}]")
    pprint({"spec_event_size": save.globals.spec_event_size})
    pprint({"spec_event_data": save.globals.spec_event_data})
    pprint({"weather_size": save.globals.weather_size})
    pprint({"weather_data": save.globals.weather_data})
    pprint({"pc_combat_count": save.globals.pc_combat_count})
    pprint({"created_num": save.globals.created_num})
    pprint({"created_records": save.globals.created_records})
    pprint({"quick_keys_size": save.globals.quick_keys_size})
    print({"quick_keys_data": save.globals.quick_keys_data})
    pprint({"reticle_size": save.globals.reticle_size})
    pprint({"reticle_data": save.globals.reticle_data})
    pprint({"interface_size": save.globals.interface_size})
    pprint({"interface_data": save.globals.interface_data})
    pprint({"regions_size": save.globals.regions_size})
    pprint({"regions_num": save.globals.regions_num})
    # pprint({"regions": save.globals.regions})

def main():
    save = OblivionSave("C:\\Users\\Czyzx\\Documents\\My Games\\Oblivion\\Saves\\autosave.ess")

    text_dump(save)


    # breakpoint()


if __name__ == "__main__":
    main()
