###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import psutil
from time import time, sleep

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class FPS_Counter():
    def __init__(self):
        self.previous_time = time()
        self.frame_count = 0
        self.FPS = 0

        # RAM memory usage
        self.process = psutil.Process(os.getpid())
        self.memory_usage = 0

    #######################################################################################################################
    
    def get_FPS(self):
        if not CONST.FPS_COUNTER: return
        if time() - self.previous_time < CONST.REFRESH_FPS_TIME: self.frame_count += 1; return

        self.FPS = self.frame_count // CONST.REFRESH_FPS_TIME
        self.previous_time = time()
        self.frame_count = 0

    #######################################################################################################################

    @staticmethod
    def get_average_FPS(FPS_array):
        if not len(FPS_array): return 0
        return int(sum(FPS_array) / len(FPS_array))

    #######################################################################################################################

    # Use in a separated thread!
    def get_memory_usage(self, shutdown_event = None):
        if isinstance(shutdown_event, type(None)): return

        while not shutdown_event.is_set():
            mem_info = self.process.memory_info()
            self.memory_usage = mem_info.rss / (1024 * 1024)
            sleep(1)

    #######################################################################################################################

    def get_directory_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try: total_size += os.path.getsize(file_path)
                # File not found (it might have been removed during the walk)
                except FileNotFoundError: pass
                # Permission error
                except PermissionError: pass
        return self.format_space_size(total_size)

    #######################################################################################################################

    def get_system_available_space(self):
        statvfs = os.statvfs('/')

        total_space = statvfs.f_frsize * statvfs.f_blocks
        available_space = statvfs.f_frsize * statvfs.f_bavail
        used_space = total_space - available_space

        return {
            'total': self.format_space_size(total_space),
            'used': self.format_space_size(used_space),
            'available': self.format_space_size(available_space),
            'available_no_format': available_space
        }
    
    #######################################################################################################################

    @staticmethod
    def format_space_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024: return f"{size:.2f}{unit}"
            size /= 1024

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    from threading import Thread, Event
    import Colored_Strings as COLOR_str

    CONST.REFRESH_FPS_TIME = 0.1
    FPS_Counter = FPS_Counter()

    previous_average_FPS = previous_FPS = 0
    max_FPS = min_FPS = 0
    FPS_array = []

    Thread(target=lambda: FPS_Counter.get_memory_usage(Event()), daemon=True).start()

    system_space = FPS_Counter.get_system_available_space()
    print('\n' + COLOR_str.SYSTEM_AVAILABLE_SPACE
        .replace('{total_space}', system_space['total'])
        .replace('{used_space}', system_space['used'])
        .replace('{available_space}', system_space['available'])
    )
    media_folder_size = FPS_Counter.get_directory_size(f'../{CONST.IMAGES_FOLDER_PATH}')
    print(COLOR_str.DIRECTORY_SIZE
        .replace('{directory}', f"'../{CONST.IMAGES_FOLDER_PATH}'")
        .replace('{size}', media_folder_size)
    )

    while True:
        FPS_Counter.get_FPS()

        if len(FPS_array) >= 100: FPS_array.pop()
        FPS_array.insert(0, FPS_Counter.FPS)
        
        average_FPS = FPS_Counter.get_average_FPS(FPS_array)

        if previous_FPS != FPS_Counter.FPS or previous_average_FPS != average_FPS:
            max_FPS = max(FPS_array) if max_FPS < max(FPS_array) else max_FPS
            min_FPS = min(FPS_array) if not min_FPS or min_FPS > min(FPS_array) else min_FPS

            
            print(COLOR_str.FPS_COUNTER
                .replace('{current_fps}', str(FPS_Counter.FPS))
                .replace('{max_fps}', str(max_FPS))
                .replace('{min_fps}', str(min_FPS))
                .replace('{average_fps}', str(average_FPS))
                .replace('{memory_usage}', f'{FPS_Counter.memory_usage:.2f}'), end='\r', flush=True
            )
            previous_FPS = FPS_Counter.FPS
            previous_average_FPS = average_FPS