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
import Constants as CONST
import Colored_Strings as COLOR_str

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
            global_playtime REAL
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
        cursor.execute('INSERT INTO General (global_encounters, global_playtime) VALUES (?, ?)', (0, 0.0))
    
    connection.commit()
    connection.close()

    print(COLOR_str.INITIALIZE_DATABASE)

###########################################################################################################################

def add_or_update_encounter(pokemon_data, local_playtime, db_file = f'./{CONST.DATABASE_PATH}'):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    # Update global stats
    cursor.execute("""
        UPDATE General SET global_encounters = global_encounters + 1, global_playtime = global_playtime + ?
    """, (local_playtime,))
    
    # Update specific pokemon stats
    cursor.execute("""
        SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?
    """, (pokemon_data['name'],))
    pokemon_info = cursor.fetchone()
    
    if pokemon_info:
        encounters, shiny_encounters = pokemon_info
        cursor.execute('''
            UPDATE Pokemon
            SET encounters = ?, shiny_encounters = ? WHERE pokemon_name = ?
        ''', (encounters + 1, shiny_encounters + 1 if pokemon_data['shiny'] else shiny_encounters, pokemon_data['name']))
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
    
    cursor.execute('SELECT global_encounters, global_playtime FROM General')
    data = cursor.fetchone()
    
    cursor.execute('SELECT pokemon_name, encounters, shiny_encounters FROM Pokemon')
    encounters = cursor.fetchall()
    
    connection.close()
    
    return {
        'global_encounters': data[0],
        'global_playtime': data[1],
        'encounters': encounters
    }

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    print()
    initialize_database(f'../{CONST.DATABASE_PATH}')
    add_or_update_encounter({'name':'Arceus', 'shiny':False}, 15843, f'../{CONST.DATABASE_PATH}')
    data = get_all_data(f'../{CONST.DATABASE_PATH}')

    hours = int(data['global_playtime']//3600)
    minutes = int((data['global_playtime'] - hours*3600)//60)
    seconds = int(data['global_playtime'] - hours*3600 - minutes*60)

    print(COLOR_str.DATABASE_INFO)
    print(COLOR_str.DATABASE_STAT_VALUE
        .replace('{stat}', '· Global Encounters')
        .replace('{value}', str(data['global_encounters']))
    )
    print(COLOR_str.DATABASE_STAT_VALUE
        .replace('{stat}', '· Global Playtime')
        .replace('{value}', f"{hours}h {minutes}min {seconds}s")
    )
    print(COLOR_str.DATABASE_STAT_VALUE
        .replace('{stat}', '· Encounters')
        .replace('{value}', "")
    )
    for index, encounter in enumerate(data['encounters']):
        print(COLOR_str.DATABASE_STAT_VALUE
            .replace('{stat}', f'\t{encounter[0]}')
            .replace('{value}', f'Encounters: {encounter[1]} - Shiny Encounters: {encounter[2]}')
        )
    print()