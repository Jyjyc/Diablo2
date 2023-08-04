import os
import errno

from datetime import datetime
from time import sleep
from shutil import copy2

def log_msg(msg, log_file_folder, print_out=True):
    """Logs msg to file and optionally prints to stdout"""


    if not os.path.exists(log_file_folder):
        os.makedirs(log_file_folder)
    
    with open(os.path.join(log_file_folder,'monitor_log.txt'), 'a') as f:
        f.write(msg + '\n')

        if print_out:
            print(msg)


def any_file_is_corrupt(save_directory, save_files, log=True):
    """Check for game character save file corruption
    
    Args:
        save_directory: str
            save file directory
        
        save_file: tup
            a tuple containing a list of file names
    
    Returns:
        is_corrupt: bool
            if any of the files is corrupt. This is because if any
            of the save files are corrupt, all files needs to be
            backed up or restored together.
    """

    # Only check .d2x and .d2s files

    corrupt = False
    for save_file, req in save_files:
        # Only checking .d2x and .d3s files
        if req:
            # If files are less than 1KB, it is corrupt
            try:
                file_sz = os.path.getsize(os.path.join(save_directory, save_file))

            except FileNotFoundError:
                file_sz = 0

            if file_sz < 1800:
                corrupt = True

            if log:
                log_msg(f'{save_file} size is {file_sz} bytes', log_file_folder, print_out=True)

    return corrupt


def copy_single_file(file_full_path, destination_directory_path):
    """Keep on trying to save a file"""
    for i in range(10):
        try:
            copy2(file_full_path, destination_directory_path)
            return
        
        except PermissionError:
            # Try again if Permission Error
            sleep(2.5)    

    # Can't copy
    log_msg(f"Failed to copy {file_full_path}", log_file_folder)


def make_backup(char_backup_path, save_files):
    """Makes character backup
    
    Args:
        char_backup_path: str
            path of character backup directory

        save_files: tup
            a tuple containing a list of character save file names
    """
  
    # Check if directory exists
    if not os.path.exists(char_backup_path):
        os.makedirs(char_backup_path)

    # Saving. .d2s and .d2x are required files, others are saved optionally
    for save_file, req in save_files: 
        file_full_path = os.path.join(save_dir, save_file)
        if req:
            copy_single_file(file_full_path, char_backup_path)
        
        else:
            try:
                copy_single_file(file_full_path, char_backup_path)
            
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

def remove_single_file(file_full_path):
    """Removes a single file which may not exist"""

    try:
        os.remove(file_full_path)
    
    except OSError as e: 
        # errno.ENOENT = no such file or directory
        if e.errno != errno.ENOENT: 
            # re-raise exception if a different error occurred
            raise 

def load_backup(char_backup_path, save_files):
    """Load character backup

    Args:
        char_backup_path: str
            path of character backup directory

        save_files: tup
            a tuple containing a list of character save file names 
    """

    # Paste backup files
    for save_file, req in save_files: 
        # Delete the save file from save directory if exists to ensure consistency
        # of save states
        bk_file_full_path = os.path.join(char_backup_path, save_file)
        plugy_save_dir = os.path.join(char_backup_path, os.pardir)
        corrupt_file_full_path = os.path.join(plugy_save_dir, save_file)
        remove_single_file(corrupt_file_full_path)

        # Copy the file
        if req:
            copy_single_file(bk_file_full_path, plugy_save_dir)
        
        # Copy non required files
        else:
            try:
                copy_single_file(bk_file_full_path, plugy_save_dir)

            except OSError as e:
                if e.errno != errno.ENOENT:
                    # re-raise exception if a different error occurred
                    raise


    # Restart Diablo 2 to prevent current currupt game state to be saved again
    # Also loads recovered game save states
    os.system("taskkill /f /im \"Game.exe\"")


if __name__ == '__main__':
    
    ####### USER SETTING #######
    char_name = "Jyc"
    save_dir = 'C:\Programs\Diablo II\save'
    log_file_folder = 'C:\Programs\Diablo II\save\Backup-Logs'
    ####### END USER SETTING #######

    char_backup_path = os.path.join(save_dir, char_name + '_bk')
    
    plugy_save_dir = os.path.join(char_backup_path, os.pardir)
    
    save_suffixse = ['.d2s', '.d2x', '.ma0', '.ma1', '.ma2', '.ma3', '.key']
    save_files_required = [True, True, False, False, False, False, False]

    save_files = [(char_name + suffix, required) for suffix, required in zip(save_suffixse, save_files_required)]
    
    save_files_required2 = [True]
    save_files2 = [('_LOD_SharedStashSave.sss', required) for suffix, required in zip(save_suffixse, save_files_required)]
	

    while True:
        if any_file_is_corrupt(save_dir, save_files):
            # File is corrupt
            load_backup(char_backup_path, save_files)
            load_backup(char_backup_path, save_files2)

            msg = "Successfully recovered at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_msg(msg, log_file_folder)
        
        else:
            # File not corrupt
            make_backup(char_backup_path, save_files)
            make_backup(char_backup_path, save_files2)
            

            msg = "Successfully backedup at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_msg(msg, log_file_folder)

        # Check again in 5 minutes
        sleep(300)            