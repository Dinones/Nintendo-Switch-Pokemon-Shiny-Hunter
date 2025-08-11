###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
from queue import Queue
from typing import Optional
from threading import Event, Thread

import Constants as CONST
from Modules.GUI import GUI, App
import Modules.Colored_Strings as STR
from Modules.FPS_Counter import FPS_Counter
from Modules.Switch_Controller import Switch_Controller
from Modules.Control_System import start_control_system, controller_control, check_threads

###########################################################################################################################
###########################################################################################################################

if __name__ == '__main__':
    # NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ: 
        print(f'\n{STR.SC_NOT_SUDO}')
        program_name = os.path.abspath(os.path.join(os.path.dirname(__file__), __file__.split('/')[-1]))
        exit(os.system(f'sudo .venv/bin/python3 {program_name}'))

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Shiny Hunter'

IMAGES_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), CONST.IMAGES_FOLDER_PATH))

###########################################################################################################################
###########################################################################################################################

def check_system_available_space(FPS: FPS_Counter) -> Optional[None]:

    """
    Check the system's available disk space and warn the user if critical thresholds are reached. Offers the option to
    delete saved images to free up space.

    Args:
        FPS (FPS_Counter): Object to get directory sizes and format available space.

    Returns:
        None
    """

    # Check the number and total size of images in the "Media/Images/" folder
    media_folder_size = FPS.get_directory_size(IMAGES_FOLDER_PATH)
    images = [
        image for image in os.listdir(IMAGES_FOLDER_PATH) if image.lower().endswith(('.png', '.jpg', 'jpeg'))
    ]

    if len(images) > CONST.IMAGES_COUNT_WARNING:
        print(STR.IMAGES_COUNT_WARNING.format(
            module=MODULE_NAME,
            images=len(images),
            path=IMAGES_FOLDER_PATH,
            size=media_folder_size
        ))

    # Check if the recycle bin size is greater than 1GB 
    recycle_bin_size = FPS.get_directory_size(os.path.expanduser('~/.local/share/Trash/files'))
    if recycle_bin_size[-2:] == 'GB':
        print(STR.USED_SPACE_WARNING.format(module=MODULE_NAME, path='Recycle Bin', size=recycle_bin_size))

    # Check whole system available space
    system_space = FPS.get_system_available_space()
    if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
        print(STR.AVAILABLE_SPACE_ERROR.format(
            module=MODULE_NAME,
            threshold=FPS.format_space_size(CONST.CRITICAL_AVAILABLE_SPACE),
            available_space=system_space['available']
        ))

        # Ask the user if wants to delete all images inside the "Media/Images/" folder
        delete = input(STR.IP_DELETE_IMAGES_QUESTION)
        if delete.lower().strip() in ('', 'y', 'yes'): 
            
            # Delete all the images
            print(STR.IP_DELETING_IMAGES.format(images=len(images)))
            for image in images:
                os.remove(f'{IMAGES_FOLDER_PATH}/{image}')
            print(STR.IP_SUCCESSFULLY_DELETED_IMAGES.format(images=len(images)))

            # Recheck the whole system available space to see if after the image deletion it's still critical
            system_space = FPS.get_system_available_space()
            if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE: 
                print(STR.AVAILABLE_SPACE_ERROR.format(
                    module=MODULE_NAME,
                    threshold=FPS.format_space_size(CONST.CRITICAL_AVAILABLE_SPACE),
                    available_space=system_space['available']
                ))
            
        else:
            exit('')

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    def main_menu():
        print('\n' + STR.M_MENU.format(module=MODULE_NAME))
        print(STR.M_MENU_OPTION.format(index=1, option='Start wild shiny hunter'))
        print(STR.M_MENU_OPTION.format(index=2, option='Start static shiny hunter'))
        print(STR.M_MENU_OPTION.format(index=3, option='Start starter shiny hunter'))
        print(STR.M_MENU_OPTION.format(index=4, option='Start Shaymin shiny hunter'))
        print(STR.M_MENU_OPTION.format(index=5, option='Start wild shiny hunter double combats (Eterna Forest)'))

        option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

        menu_options = {
            '1': shiny_hunter,
            '2': shiny_hunter,
            '3': shiny_hunter,
            '4': shiny_hunter,
            '5': shiny_hunter,
        }

        # Set XDG_RUNTIME_DIR and ALSOFT_LOGLEVEL environment variable (avoid unnecessary warnings)
        os.environ['XDG_RUNTIME_DIR'] = "/tmp/runtime-root"
        os.makedirs(os.environ['XDG_RUNTIME_DIR'], exist_ok=True)
        os.chmod(os.environ['XDG_RUNTIME_DIR'], 0o700)
        os.environ['ALSOFT_LOGLEVEL'] = '0'

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME))
    
    #######################################################################################################################
    #######################################################################################################################

    def shiny_hunter(option):
        if option == '1': action = 'wild'
        elif option == '2': action = 'static'
        elif option == '3': action = 'starter'
        elif option == '4': action = 'Shaymin'
        elif option == '5': action = 'wild (double combats)'

        print('\n' + STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action=f"Starting {action} shiny hunter...",
            path=''
        ))

        ###################################################################################################################
        ###################################################################################################################
        
        FPS = FPS_Counter()
        check_system_available_space(FPS)

        # Used to send data from the control system to the GUI
        Image_Queue = Queue()
        Controller = Switch_Controller()

        shutdown_event = Event()
        stop_event = Event()

        ###################################################################################################################
        ###################################################################################################################

        if option == '1': encounter_type = 'WILD'
        elif option == '2': encounter_type = 'STATIC'
        elif option == '3': encounter_type = 'STARTER'
        elif option == '4': encounter_type = 'SHAYMIN'
        elif option == '5': encounter_type = 'WILD_DOUBLES'

        threads = []
        threads.append({
            'function': 'control_system',
            'thread': Thread(target=lambda: 
                start_control_system(encounter_type, FPS, Controller, Image_Queue, shutdown_event, stop_event),
                daemon=True
            )
        })

        threads.append({
            'function': 'get_memory_usage',
            'thread': Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True)
        })

        threads.append({
            'function': 'controller_control',
            'thread': Thread(target=lambda: controller_control(Controller, shutdown_event), daemon=True)
        })

        threads.append({
            'function': 'check_threads',
            'thread': Thread(target=lambda: check_threads(threads, shutdown_event), daemon=True)
        })

        # Start all threads
        for thread in threads:
            thread['thread'].start()

        GUI_App = App()
        User_Interface = GUI(Image_Queue, shutdown_event, stop_event)
        # Blocking function until the GUI is closed
        GUI_App.exec_()

        shutdown_event.set()

        print(STR.G_RELEASING_THREADS.format(module=MODULE_NAME, threads=len(threads)))

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()