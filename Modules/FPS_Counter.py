###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from __future__ import annotations

import os
import sys
import psutil
from time import time
from typing import TYPE_CHECKING, Optional, List, Dict, Union

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST

if TYPE_CHECKING:
    import threading

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class FPS_Counter():
    def __init__(self):

        """
        Initializes FPS tracking and system resource usage monitoring.
        """

        self.previous_time = time()
        self.frame_count = 0
        self.FPS = 0

        self.process = psutil.Process(os.getpid())
        self.memory_usage = 0 # RAM
        self.cpu_usage = 0 
        self.cores = psutil.cpu_count()

    #######################################################################################################################
    #######################################################################################################################
    
    def get_FPS(self) -> None:

        """
        Obtains the FPS value based on the elapsed time.

        Returns:
            None
        """

        # Skip if FPS tracking is disabled
        if not CONST.FPS_COUNTER:
            return

        # If within the refresh window, just increment the frame counter
        if time() - self.previous_time < CONST.REFRESH_FPS_TIME:
            self.frame_count += 1
            return

        # Calculate FPS, reset timer and counter
        self.FPS = self.frame_count // CONST.REFRESH_FPS_TIME
        self.previous_time = time()
        self.frame_count = 0

    #######################################################################################################################
    #######################################################################################################################

    def get_memory_usage(self, shutdown_event: Optional[threading.Event] = None) -> None:

        """
        Continuously updates memory and CPU usage while the thread runs. This method is intended to be run in a separate
        thread. It will stop when "shutdown_event" is set.

        Args:
            shutdown_event (Optional[threading.Event]): Event used to signal termination of the loop.

        Returns:
            None
        """

        if shutdown_event is None:
            return

        while not shutdown_event.is_set():
            # RAM usage in MB
            self.memory_usage = self.process.memory_info().rss / (1024 * 1024)

            # Normalize CPU usage by number of cores to keep range [0, 100]
            self.cpu_usage = self.process.cpu_percent(interval=1) / self.cores

    #######################################################################################################################
    #######################################################################################################################

    def get_directory_size(self, path: str) -> str:

        """
        Calculates the total size of all files within a directory and its subdirectories.

        Args:
            path (str): The path to the directory.

        Returns:
            str: The total size formatted as a human-readable string (e.g. '12.45MB').
        """

        total_size = 0

        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except FileNotFoundError:
                    # File was removed during walk
                    pass
                except PermissionError:
                    # No read permission on file
                    pass

        return self._format_space_size(total_size)

    #######################################################################################################################
    #######################################################################################################################

    def get_system_available_space(self) -> Dict[str, Union[str, int]]:

        """
        Retrieves disk space information for the root filesystem.

        Returns:
            Dict[str, Union[str, int]]: A dictionary containing:
                - 'total': Formatted total disk space
                - 'used': Formatted used disk space
                - 'available': Formatted available space
                - 'available_no_format': Raw available bytes (int)
        """

        statvfs = os.statvfs('/')

        # Byte size = fragment size * number of blocks
        total_space = statvfs.f_frsize * statvfs.f_blocks
        available_space = statvfs.f_frsize * statvfs.f_bavail
        used_space = total_space - available_space

        return {
            'total': self._format_space_size(total_space),
            'used': self._format_space_size(used_space),
            'available': self._format_space_size(available_space),
            'available_no_format': available_space
        }
    
    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def _format_space_size(size: float) -> str:

        """
        Converts a byte size into a human-readable format (B, KB, MB, GB, etc.).

        Args:
            size (float): The size in bytes.

        Returns:
            str: A formatted string with two decimal places and the appropriate unit.
        """

        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024 or unit == 'TB':
                return f"{size:.2f}{unit}"
            size /= 1024

    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def _get_average_FPS(FPS_array: List[int]) -> int:

        """
        Calculates the average FPS from a list of recorded FPS values. Only used for debugging.

        Args:
            FPS_array (List[int]): A list of FPS integers.

        Returns:
            int: The average FPS, or 0 if the list is empty.
        """

        if not FPS_array:
            return 0
        return int(sum(FPS_array) / len(FPS_array))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import Debug.FPS_Counter_Debug