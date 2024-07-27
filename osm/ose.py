import os

from pprint import pprint

from oblivion_save import *
# from helpers import FileReader, PCLocation, Record, ChangeRecord



def main():
    save = OblivionSave("C:\\Users\\Czyzx\\Documents\\My Games\\Oblivion\\Saves\\autosave.ess")
    
    pprint(save.file_header)
    pprint(save.save_header.screenshot.width)
    pprint(save.plugins)

    # breakpoint()

if __name__ == "__main__":
    main()
