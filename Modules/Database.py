###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import sqlite3
from typing import Dict, Union, Tuple, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Modules.Colored_Strings as STR
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.DATABASE_PATH))

###########################################################################################################################
###########################################################################################################################

def initialize_database(db_file: str = DATABASE_PATH) -> None:

    """
    Initializes the SQLite database with required tables and default values.

    Args:
        db_file (str): Path to the SQLite database file.

    Returns:
        None
    """

    # Connect to the database (creates it if it doesn't exist)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Create "General" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS General (
            global_encounters INTEGER,
            global_playtime REAL,
            last_shiny_encounter INTEGER,
            global_shinies_found INTEGER
        )
    ''')

    # Create "Pokemon" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pokemon (
            pokemon_name TEXT NOT NULL,
            shiny_encounters INTEGER,
            encounters INTEGER
        )
    ''')

    # Populate default row in General if empty
    cursor.execute('SELECT COUNT(*) FROM General')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO General (
                global_encounters, global_playtime, last_shiny_encounter, global_shinies_found
            ) VALUES (?, ?, ?, ?)
        ''', (0, 0.0, 0, 0))

    # Finalize and close
    connection.commit()
    connection.close()

    print(STR.DB_INITIALIZE_DATABASE)

###########################################################################################################################
###########################################################################################################################

def add_or_update_encounter(
    pokemon_data: Dict[str, Union[str, bool]],
    local_playtime: float,
    db_file: str = DATABASE_PATH
) -> None:

    """
    Updates the database with the result of an encounter.

    Args:
        pokemon_data (Dict[str, Union[str, bool]]): Contains:
            - 'name' (str): The Pokémon name.
            - 'shiny' (bool): Whether the Pokémon is shiny.
        local_playtime (float): Time (in seconds or minutes) to add to total playtime.
        db_file (str): Path to the SQLite database.

    Returns:
        None
    """

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Fetch current global stats
    cursor.execute("SELECT global_encounters, last_shiny_encounter FROM General")
    global_encounters, last_shiny_encounter = cursor.fetchone()

    # Determine values to add/update
    is_shiny = pokemon_data['shiny']
    new_last_shiny = global_encounters if is_shiny else last_shiny_encounter
    shiny_increment = 1 if is_shiny else 0
    encounter_increment = 0 if is_shiny else 1  # don't increment shiny encounter count twice

    # Update General table
    cursor.execute("""
        UPDATE General
        SET global_encounters = global_encounters + ?,
            global_playtime = global_playtime + ?,
            last_shiny_encounter = ?,
            global_shinies_found = global_shinies_found + ?
    """, (encounter_increment, local_playtime, new_last_shiny, shiny_increment))

    # Fetch Pokémon-specific stats (if any)
    cursor.execute("""
        SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?
    """, (pokemon_data['name'],))
    pokemon_info = cursor.fetchone()

    if pokemon_info:
        encounters, shiny_encounters = pokemon_info
        updated_encounters = encounters + 1 if not is_shiny else encounters
        updated_shinies = shiny_encounters + 1 if is_shiny else shiny_encounters

        cursor.execute('''
            UPDATE Pokemon
            SET encounters = ?, shiny_encounters = ?
            WHERE pokemon_name = ?
        ''', (updated_encounters, updated_shinies, pokemon_data['name']))
    else:
        # Insert new Pokémon entry
        cursor.execute('''
            INSERT INTO Pokemon (pokemon_name, encounters, shiny_encounters)
            VALUES (?, ?, ?)
        ''', (pokemon_data['name'], 1, 1 if is_shiny else 0))

    connection.commit()
    connection.close()

###########################################################################################################################
###########################################################################################################################

def get_all_data(db_file: str = DATABASE_PATH) -> Dict[str, Union[int, float, List[Tuple[str, int, int]]]]:

    """
    Retrieves all relevant encounter and playtime data from the database.

    Args:
        db_file (str): Path to the SQLite database. Defaults to DATABASE_PATH.

    Returns:
        Dict[str, Union[int, float, List[Tuple]]]: A dictionary containing:
            - 'global_encounters': Total number of non-shiny encounters
            - 'global_playtime': Total playtime
            - 'global_shinies_found': Total number of shiny Pokémon found
            - 'last_shiny_encounter': The encounter number of the last shiny
            - 'encounters': A list of tuples (pokemon_name, total_encounters, shiny_encounters)
    """

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Read global stats
    cursor.execute('''
        SELECT global_encounters, global_playtime, last_shiny_encounter, global_shinies_found
        FROM General
    ''')
    data = cursor.fetchone() or (0, 0.0, 0, 0)

    # Read all per-pokémon encounters
    cursor.execute('''
        SELECT pokemon_name, encounters, shiny_encounters FROM Pokemon
    ''')
    encounters = cursor.fetchall()

    connection.close()

    return {
        'global_encounters': data[0],
        'global_playtime': data[1],
        'global_shinies_found': data[3],
        'last_shiny_encounter': data[2],
        'encounters': encounters
    }

###########################################################################################################################
###########################################################################################################################

def delete_pokemon_database(pokemon: str, db_file: str = DATABASE_PATH) -> None:

    """
    Deletes a specific Pokémon's encounter data from the database and adjusts global stats accordingly.

    Args:
        pokemon (str): The name of the Pokémon to delete.
        db_file (str): Path to the SQLite database. Defaults to CONST.DATABASE_PATH.

    Returns:
        None
    """

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Check if the Pokémon exists in the database
    cursor.execute('''
        SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?
    ''', (pokemon,))
    pokemon_info = cursor.fetchone()

    if pokemon_info is None:
        print(STR.DB_COULD_NOT_DELETE_POKEMON.replace('{pokemon}', pokemon), end="\n")
        connection.close()
        return

    total_encounters, shiny_encounters = pokemon_info

    # Update global stats accordingly (only if General has a known primary key row — assumed to be id=1)
    cursor.execute('''
        UPDATE General
        SET global_encounters = global_encounters - ?,
            global_shinies_found = global_shinies_found - ?
        WHERE rowid = 1
    ''', (total_encounters, shiny_encounters))

    # Delete the Pokémon from the database
    cursor.execute('''
        DELETE FROM Pokemon WHERE pokemon_name = ?
    ''', (pokemon,))

    connection.commit()
    connection.close()

    print(STR.DB_POKEMON_DELETED.format(pokemon=pokemon))

###########################################################################################################################
###########################################################################################################################

def decrement_pokemon_shiny(pokemon: str, db_file: str = DATABASE_PATH) -> None:

    """
    Subtracts one shiny encounter from the specified Pokémon and updates global shiny stats accordingly. If the Pokémon has
    no shiny encounters, the function does nothing.

    Args:
        pokemon (str): The name of the Pokémon to update.
        db_file (str): Path to the SQLite database.

    Returns:
        None
    """

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Fetch current shiny encounter count for the Pokémon
    cursor.execute('''
        SELECT shiny_encounters FROM Pokemon WHERE pokemon_name = ?
    ''', (pokemon,))
    result = cursor.fetchone()

    if result is None:
        print(STR.DB_COULD_NOT_DELETE_POKEMON.replace('{pokemon}', pokemon), end="\n\n")
        connection.close()
        return

    shiny_encounters = result[0]

    # Do nothing if shiny count is already zero
    if shiny_encounters <= 0:
        print(f"[INFO] Pokémon '{pokemon}' has no shiny encounters to remove.\n")
        connection.close()
        return

    # Decrement shiny count in Pokémon table
    cursor.execute('''
        UPDATE Pokemon SET shiny_encounters = shiny_encounters - 1 WHERE pokemon_name = ?
    ''', (pokemon,))

    # Decrement global shiny count
    cursor.execute('''
        UPDATE General SET global_shinies_found = global_shinies_found - 1
    ''')

    connection.commit()
    connection.close()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

# if __name__ == "__main__":
#     def main_menu():
#         print('\n' + STR.M_MENU.replace('{module}', 'Database'))
#         print(STR.M_MENU_OPTION.replace('{index}', '1').replace('{option}', 'Print database'))
#         print(STR.M_MENU_OPTION.replace('{index}', '2').replace('{option}', 'Print testing database'))
#         print(STR.M_MENU_OPTION.replace('{index}', '3').replace('{option}', 'Delete pokémon from database'))

#         option = input('\n' + STR.M_OPTION_SELECTION.replace('{module}', 'Database'))

#         menu_options = {
#             '1': print_database,
#             '2': print_database,
#             '3': delete_pokemon,
#         }

#         if option in menu_options: menu_options[option](option)
#         else: print(STR.M_INVALID_OPTION.replace('{module}', 'Database') + '\n')

#     #######################################################################################################################
#     #######################################################################################################################
    
#     def print_database(option):
#         if option == '2': action = 'test'
#         else: action = 'normal'
#         print('\n' + STR.M_SELECTED_OPTION
#             .replace('{module}', 'Database')
#             .replace('{option}', f"{option}")
#             .replace('{action}', f"Printing {'testing ' if action == 'test' else ''}database...")
#             .replace('{path}', '')
#         )

#         print()
#         path = f'../{CONST.DATABASE_PATH}' if action == 'normal' else f'../{CONST.TESTING_DATABASE_PATH}'
#         initialize_database(path)
#         if action == 'test':
#             # The shiny one doesn't add an encounter to the global encounters of the pokemon
#             # because the main program would add the encounter twice
#             add_or_update_encounter({'name': 'Arceus', 'shiny': True}, 15843, f'../{CONST.TESTING_DATABASE_PATH}')
#         data = get_all_data(path)

#         days = int(data['global_playtime']//86400)
#         hours = int((data['global_playtime'] - days*86400)//3600)
#         minutes = int((data['global_playtime'] - days*86400 - hours*3600)//60)
#         seconds = int(data['global_playtime'] - days*86400 - hours*3600 - minutes*60)

#         print(STR.DB_DATABASE_INFO)
#         for key in data.keys():
#             aux_key = ''
#             for word in key.split('_'): aux_key += word.capitalize() + ' '
#             aux_key = aux_key.strip()
            
#             value = str(data[key])
#             if key == 'global_playtime': value = f"{days}d {hours}h {minutes}min {seconds}s"
#             elif key == 'encounters': value = ''

#             print(STR.DB_DATABASE_STAT_VALUE
#                 .replace('{stat}', f'· {aux_key}')
#                 .replace('{value}', value)
#             )

#         for index, encounter in enumerate(data['encounters']):
#             print(STR.DB_DATABASE_STAT_VALUE
#                 .replace('{stat}', f'\t{encounter[0]}')
#                 .replace('{value}', f'Encounters: {encounter[1]} - Shiny Encounters: {encounter[2]}')
#             )
#         print()

#     #######################################################################################################################
#     #######################################################################################################################

#     def delete_pokemon(option):
#         print_database(str(3))
#         print(STR.DB_SELECT_POKEMON_TO_DELETE, end = '')
#         pokemon = input()
#         delete_pokemon_database(pokemon, f'../{CONST.DATABASE_PATH}')

#     #######################################################################################################################
#     #######################################################################################################################

#     main_menu()