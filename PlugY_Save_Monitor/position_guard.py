import os
import time
import platform
import errno

from datetime import datetime
from shutil import copy2

if __name__ == '__main__':

    ####### USER SETTING #######
    char_name = "jyc"
    char2_name = "fsdfa"
#    if platform.system() == 'Linux':
#        save_dir = '/mnt/c/Users/victo/Dropbox (Personal)/D2Save'
#    else if platform.system() == 'Windows'
    save_dir = 'C:\Programs\Diablo II\save'

    # Specify char name and position on select screen
    #chars = [(char1_name, 1), (char2_name, 2)]
    ####### END USER SETTING #######

    #save_suffixes = ['.d2s', '.d2x', '.ma0', '.ma1', '.ma2', '.ma3', '.key']
    save_suffixes = ['.d2s', '.d2x', '.ma0', '.key']

    start_time = time.time()
    while True:
        target_time = start_time - 0 * 1000
        for suffix in save_suffixes:
            file_path = os.path.join(save_dir, char_name + suffix)
            mod_time = os.path.getmtime(file_path) 
            if mod_time != target_time:
                print('modified ', file_path)
                os.utime(file_path, (target_time, target_time))

#    start_time = time.time()
#    while True:
#        for char, position in chars:
#            target_time = start_time - position * 1000
#            for suffix in save_suffixes:
#                file_path = os.path.join(save_dir, char + suffix)
#                mod_time = os.path.getmtime(file_path) 
#                if mod_time != target_time:
#                    print('modified ', file_path)
#                    os.utime(file_path, (target_time, target_time))
        time.sleep(1.5)

