# PlugY Save Monitor
![bg](https://user-images.githubusercontent.com/15576531/61544030-92c49200-aa12-11e9-8ffc-62fa3226e5ff.jpg)

Prevent Diablo II mod PlugY from corrupting saved games through automated interval backup and restore.

## How It Works
PlugY is not a 100% stable mod and it crashes quite often. For me, the frequency is around once every few hours. When the crash happens, the game sometimes overwrites the character stash save file `char_name.d2s` with an empty file of under 1KB in size. This causes all of your items in your stash to disappear.

The script monitors for the file size of the save files, and when the file size goes under ~1KB, it will restore the backed up saved game files.

Note that for the restore operation to complete, we will need to terminate `Game.exe` and reload the backup save files. *If you are running Diablo with admin privileges, you will NOT be able to terminate the game without also running this script /w admin privileges.*

In other words, if you are botting with D2ETAL you will need to run the script /w admin privilege.

## Quick Start
Open `plugy_save_monitor.py` with text editor and change the save file path. 

You can run the script afterwards with `python -m plugy_save_monitor`.

This script has no external dependencies.

## Author
Victor Xu

## License
MIT
