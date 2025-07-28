###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
from threading import Thread, Event

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
import Modules.Colored_Strings as STR
from Modules.FPS_Counter import FPS_Counter

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

CONST.REFRESH_FPS_TIME = 0.1
FPS_Counter = FPS_Counter()

previous_average_FPS = previous_FPS = 0
max_FPS = min_FPS = 0
FPS_array = []

# Start the system monitoring thread (memory and CPU usage). Runs in the background until the main program exits
Thread(target=lambda: FPS_Counter.get_memory_usage(Event()), daemon=True).start()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

# Print available disk space
system_space = FPS_Counter.get_system_available_space()
print('\n' + STR.FPS_SYSTEM_AVAILABLE_SPACE
    .replace('{total_space}', system_space['total'])
    .replace('{used_space}', system_space['used'])
    .replace('{available_space}', system_space['available'])
)

# Print size of the Media directory
media_folder_size = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Media'))
print(STR.FPS_DIRECTORY_SIZE
    .replace('{directory}', f"'../Media/'")
    .replace('{size}', media_folder_size)
)

# Print size of the local Recycle Bin
recycle_bin_size = FPS_Counter.get_directory_size(os.path.expanduser('~/.local/share/Trash/files'))
print(STR.FPS_DIRECTORY_SIZE
    .replace('{directory}', f"'{os.path.expanduser('~/.local/share/Trash/files')}'")
    .replace('{size}', recycle_bin_size)
)

while True:
    FPS_Counter.get_FPS()

    # Maintain only the most recent 100 FPS samples
    if len(FPS_array) >= 100:
        FPS_array.pop()
    FPS_array.insert(0, FPS_Counter.FPS)

    # Calculate average FPS from the collected values
    average_FPS = FPS_Counter._get_average_FPS(FPS_array)

    # Only print if values have changed
    if previous_FPS != FPS_Counter.FPS or previous_average_FPS != average_FPS:
        # Update max and min FPS seen so far
        max_FPS = max(FPS_array) if max_FPS < max(FPS_array) else max_FPS
        min_FPS = min(FPS_array) if not min_FPS or min_FPS > min(FPS_array) else min_FPS

        # Print live FPS and memory usage display
        print(STR.FPS_COUNTER
            .replace('{current_fps}', str(FPS_Counter.FPS))
            .replace('{max_fps}', str(max_FPS))
            .replace('{min_fps}', str(min_FPS))
            .replace('{average_fps}', str(average_FPS))
            .replace('{memory_usage}', f'{FPS_Counter.memory_usage:.2f}'), end='\r', flush=True
        )

        # Update reference values to detect changes in the next loop
        previous_FPS = FPS_Counter.FPS
        previous_average_FPS = average_FPS