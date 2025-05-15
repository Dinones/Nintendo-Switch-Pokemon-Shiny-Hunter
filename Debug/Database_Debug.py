###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
from Modules.Database import *
import Modules.Colored_Strings as COLOR_str
from Modules.FPS_Counter import FPS_Counter

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Database'
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.DATABASE_PATH))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    def main_menu():
        print('\n' + COLOR_str.M_MENU.replace('{module}', MODULE_NAME))
        print(COLOR_str.M_MENU_OPTION.replace('{index}', '1').replace('{option}', 'Print database'))
        print(COLOR_str.M_MENU_OPTION.replace('{index}', '2').replace('{option}', 'Remove Pokémon'))

        option = input('\n' + COLOR_str.M_OPTION_SELECTION.replace('{module}', MODULE_NAME))

        menu_options = {
            '1': _print_database,
            '2': _delete_pokemon,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.M_INVALID_OPTION.replace('{module}', MODULE_NAME) + '\n')
    
    #######################################################################################################################
    #######################################################################################################################
    
    def _print_database(option):
        print('\n' + STR.M_SELECTED_OPTION
            .replace('{module}', MODULE_NAME)
            .replace('{option}', f"{option}")
            .replace('{action}', f"Printing database...")
            .replace('{path}', '')
        )

        initialize_database(DATABASE_PATH)
        data = get_all_data(DATABASE_PATH)

        days = int(data['global_playtime']//86400)
        hours = int((data['global_playtime'] - days*86400)//3600)
        minutes = int((data['global_playtime'] - days*86400 - hours*3600)//60)
        seconds = int(data['global_playtime'] - days*86400 - hours*3600 - minutes*60)

        print(STR.DB_DATABASE_INFO)
        for key in data.keys():
            aux_key = ''
            for word in key.split('_'): aux_key += word.capitalize() + ' '
            aux_key = aux_key.strip()
            
            value = str(data[key])
            if key == 'global_playtime': value = f"{days}d {hours}h {minutes}min {seconds}s"
            elif key == 'encounters': value = ''

            print(STR.DB_DATABASE_STAT_VALUE
                .replace('{stat}', f'· {aux_key}')
                .replace('{value}', value)
            )

        for index, encounter in enumerate(data['encounters']):
            print(STR.DB_DATABASE_STAT_VALUE
                .replace('{stat}', f'\t{encounter[0]}')
                .replace('{value}', f'Encounters: {encounter[1]} - Shiny Encounters: {encounter[2]}')
            )

    #######################################################################################################################
    #######################################################################################################################

    def _delete_pokemon(option: str) -> None:

        """
        Handles the irreversible deletion of a Pokémon from the database.

        Args:
            option (str): Menu option or context for display purposes (e.g., "3").

        Returns:
            None
        """

        _print_database(option)

        print(f'\n{STR.DB_SELECT_POKEMON_TO_DELETE}', end='')
        pokemon = input().strip()

        # Confirm irreversible action
        print(f"\n{STR.DB_ASK_POKEMON_TO_DELETE.format(pokemon=pokemon)}", end='')
        confirmation = input().strip().lower()

        if confirmation in ('yes', 'y'):
            delete_pokemon_database(pokemon, DATABASE_PATH)
        else:
            print(STR.DB_DELETION_CANCELLED)

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()