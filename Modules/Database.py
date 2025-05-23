###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import sqlite3

import sys; sys.path.append('..')
import Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def initialize_database(db_file = f'./{CONST.DATABASE_PATH}'):
    # Connect to the database (create it if it doesn't exist)
    connection = sqlite3.connect(db_file)
    # Used to execute SQL commands
    cursor = connection.cursor()
    
    # Create a table for general details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS General (
            global_encounters INTEGER,
            global_playtime REAL,
            last_shiny_encounter INTEGER,
            global_shinies_found INTEGER
        )
    ''')
    
    # Create a table for encounter details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pokemon (
            pokemon_name TEXT NOT NULL,
            shiny_encounters INTEGER,
            encounters INTEGER
        )
    ''')
    
    # Initialize General table with default values if it's empty
    cursor.execute('SELECT COUNT(*) FROM General')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO General (global_encounters, global_playtime, last_shiny_encounter, global_shinies_found) 
            VALUES (?, ?, ?, ?)
        ''', (0, 0.0, 0, 0))
    
    connection.commit()
    connection.close()

    print(COLOR_str.INITIALIZE_DATABASE)

###########################################################################################################################


def add_or_update_encounter(pokemon_data, local_playtime, db_file = f'./{CONST.DATABASE_PATH}'):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    # Update global stats
    cursor.execute("""SELECT global_encounters, last_shiny_encounter FROM General""")
    encounters = cursor.fetchone()
    global_encounters, last_shiny_encounter = encounters[0], encounters[1]
    cursor.execute("""
        UPDATE General SET global_encounters = global_encounters + ?, global_playtime = global_playtime + ?,
        last_shiny_encounter = ?, global_shinies_found = global_shinies_found + ?
    """, (0 if pokemon_data['shiny'] else 1, local_playtime, global_encounters if 
        pokemon_data['shiny'] else last_shiny_encounter, 1 if pokemon_data['shiny'] else 0
    ))
    
    # Update specific pokemon stats
    cursor.execute("""
        SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?
    """, (pokemon_data['name'],))
    pokemon_info = cursor.fetchone()
    
    if pokemon_info:
        encounters, shiny_encounters = pokemon_info
        # If the pokemon is shiny the encounter would be added twice
        cursor.execute('''
            UPDATE Pokemon
            SET encounters = ?, shiny_encounters = ? WHERE pokemon_name = ?
        ''', (encounters + 1 if not pokemon_data['shiny'] else encounters, 
            shiny_encounters + 1 if pokemon_data['shiny'] else shiny_encounters, pokemon_data['name']))
    else:
        cursor.execute('''
            INSERT INTO Pokemon (pokemon_name, encounters, shiny_encounters)
            VALUES (?, ?, ?)
        ''', (pokemon_data['name'], 1, 1 if pokemon_data['shiny'] else 0))
    
    connection.commit()
    connection.close()

###########################################################################################################################

def get_all_data(db_file = f'./{CONST.DATABASE_PATH}'):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    cursor.execute('SELECT global_encounters, global_playtime, last_shiny_encounter, global_shinies_found FROM General')
    data = cursor.fetchone()
    
    cursor.execute('SELECT pokemon_name, encounters, shiny_encounters FROM Pokemon')
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

def delete_pokemon_database(pokemon, db_file = f'./{CONST.DATABASE_PATH}'):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Check if the pokemon exists in the database
    cursor.execute("""
        SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?
    """, (pokemon,))
    pokemon_info = cursor.fetchone()

    if type(pokemon_info) == type(None): 
        print(COLOR_str.COULD_NOT_DELETE_POKEMON.replace('{pokemon}', pokemon), end=2*'\n')
        return

    # Update global stats
    cursor.execute("""
        UPDATE General SET global_encounters = global_encounters - ?, global_shinies_found = global_shinies_found - ?
    """, (pokemon_info[0], pokemon_info[1]))

    # Delete specific pokémon info
    cursor.execute("""
        DELETE FROM Pokemon WHERE pokemon_name = ?
    """, (pokemon,))

    connection.commit()
    connection.close()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Database'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Print database'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Print testing database'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '3').replace('{option}', 'Delete pokémon from database'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Database'))

        menu_options = {
            '1': print_database,
            '2': print_database,
            '3': delete_pokemon,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Database') + '\n')

    #######################################################################################################################
    #######################################################################################################################
    
    def print_database(option):
        if option == '2': action = 'test'
        else: action = 'normal'
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Database')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Printing {'testing ' if action == 'test' else ''}database...")
            .replace('{path}', '')
        )

        print()
        path = f'../{CONST.DATABASE_PATH}' if action == 'normal' else f'../{CONST.TESTING_DATABASE_PATH}'
        initialize_database(path)
        if action == 'test':
            # The shiny one doesn't add an encounter to the global encounters of the pokemon
            # because the main program would add the encounter twice
            add_or_update_encounter({'name': 'Arceus', 'shiny': True}, 15843, f'../{CONST.TESTING_DATABASE_PATH}')
        data = get_all_data(path)

        days = int(data['global_playtime']//86400)
        hours = int((data['global_playtime'] - days*86400)//3600)
        minutes = int((data['global_playtime'] - days*86400 - hours*3600)//60)
        seconds = int(data['global_playtime'] - days*86400 - hours*3600 - minutes*60)

        print(COLOR_str.DATABASE_INFO)
        for key in data.keys():
            aux_key = ''
            for word in key.split('_'): aux_key += word.capitalize() + ' '
            aux_key = aux_key.strip()
            
            value = str(data[key])
            if key == 'global_playtime': value = f"{days}d {hours}h {minutes}min {seconds}s"
            elif key == 'encounters': value = ''

            print(COLOR_str.DATABASE_STAT_VALUE
                .replace('{stat}', f'· {aux_key}')
                .replace('{value}', value)
            )

        for index, encounter in enumerate(data['encounters']):
            print(COLOR_str.DATABASE_STAT_VALUE
                .replace('{stat}', f'\t{encounter[0]}')
                .replace('{value}', f'Encounters: {encounter[1]} - Shiny Encounters: {encounter[2]}')
            )
        print()

    #######################################################################################################################
    #######################################################################################################################

    def delete_pokemon(option):
        print_database(str(3))
        print(COLOR_str.SELECT_POKEMON_TO_DELETE, end = '')
        pokemon = input()
        delete_pokemon_database(pokemon, f'../{CONST.DATABASE_PATH}')

    #######################################################################################################################

    main_menu()