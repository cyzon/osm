import os

from pprint import pprint

from oblivion_save import *
# from helpers import FileReader, PCLocation, Record, ChangeRecord



def main():
    save = OblivionSave("C:\\Users\\Czyzx\\Documents\\My Games\\Oblivion\\Saves\\autosave.ess")
    
    # pprint(save.file_header)
    # pprint(save.save_header)
    # pprint(save.plugins)
    # pprint(save.globals)
    # for cr in save.globals.created_records:
        # print(cr)
    # pprint(save.change_records)
    # pprint(save.temporary_effects)
    # pprint(save.form_ids)
    # pprint(save.worldspaces)

    # breakpoint()


if __name__ == "__main__":
    main()
