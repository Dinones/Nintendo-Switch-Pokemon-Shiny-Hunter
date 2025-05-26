###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import json
import unittest
from parameterized import parameterized_class

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Modules.Database import *

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Define absolute paths to required resources
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.TESTING_DATABASE_PATH))
TESTS_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tests Data/Database_Data.json'))

# Load test case definitions from JSON
with open(TESTS_DATA_FILE, 'r') as file: 
    TEST_DATA = json.load(file)

###########################################################################################################################
###########################################################################################################################

@parameterized_class(TEST_DATA)
class Test_Database(unittest.TestCase):
    def setUp(self) -> None:

        """
        Prepares a clean test environment before each test case. Deletes the test database file if it already exists to
        ensure test isolation. Re-initializes the database to a known default.
        """

        # Ensure the test DB does not exist before each test run
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)

        # Create a fresh database with the expected structure
        initialize_database(DATABASE_PATH)

    #######################################################################################################################
    #######################################################################################################################

    def test_initialize_database(self) -> None:

        """
        Tests that the database is initialized correctly with the required structure and default values.

        Asserts:
            - 'General' table is present in the database.
            - 'Pokemon' table is present in the database.
            - 'General' table contains a single row with values: (0, 0.0, 0, 0)
        """

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Check that both tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        self.assertIn("General", tables)
        self.assertIn("Pokemon", tables)

        # Check that default row exists in General table
        cursor.execute("SELECT * FROM General")
        general_row = cursor.fetchone()
        self.assertIsNotNone(general_row)
        self.assertEqual(general_row, (0, 0.0, 0, 0))

        conn.close()

    #######################################################################################################################
    #######################################################################################################################

    def test_add_non_shiny(self) -> None:

        """
        Tests that a non-shiny encounter is properly added to the database.

        Asserts:
            - General table has 1 global encounter, total playtime matches input, and 0 shinies found.
            - Pokémon table for Pikachu has 1 encounter, 0 shiny encounters.
        """

        pokemon = {'name': 'Pikachu', 'shiny': False}
        playtime = 10.5

        # Add non-shiny encounter
        add_or_update_encounter(pokemon, playtime, DATABASE_PATH)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Check General table for global stats
        cursor.execute("SELECT global_encounters, global_playtime, global_shinies_found FROM General")
        general = cursor.fetchone()
        self.assertEqual(general, (1, playtime, 0))

        # Check Pokémon table for Pikachu stats
        cursor.execute("SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?", (pokemon['name'],))
        pikachu = cursor.fetchone()
        self.assertEqual(pikachu, (1, 0))

        conn.close()

    #######################################################################################################################
    #######################################################################################################################

    def test_add_shiny(self) -> None:

        """
        Tests that a shiny and non-shiny encounter for the same Pokémon is handled correctly.

        Asserts:
            - General table shows 1 total encounter (normal), 1 shiny found, and total playtime is correctly accumulated.
            - Pokémon table shows 1 total encounter and 1 shiny encounter for 'Charmander'.
        """

        playtime = 5.0
        pokemon = {'name': 'Charmander'}

        # Add shiny encounter
        add_or_update_encounter({**pokemon, 'shiny': False}, playtime, DATABASE_PATH)
        add_or_update_encounter({**pokemon, 'shiny': True}, playtime, DATABASE_PATH)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Check General table: only non-shiny encounter increments global_encounters
        cursor.execute("SELECT global_encounters, global_playtime, global_shinies_found FROM General")
        general = cursor.fetchone()
        self.assertEqual(general, (1, 2 * playtime, 1))

        # Check Pokémon table: 1 encounter total, and it was shiny
        cursor.execute("SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?", (pokemon['name'],))
        charmander = cursor.fetchone()
        self.assertEqual(charmander, (1, 1))

        conn.close()

    #######################################################################################################################
    #######################################################################################################################

    def test_delete_pokemon_database(self) -> None:

        """
        Tests that a Pokémon can be deleted from the database and global stats are updated accordingly.

        Asserts:
            - Pokémon is removed from the database.
            - General stats reflect the removal of the encounters and shiny count.
        """

        pokemon = {'name': 'Bulbasaur', 'shiny': False}
        playtime = 7.0

        # Add the Pokémon first
        add_or_update_encounter(pokemon, playtime, DATABASE_PATH)

        # Confirm it was added
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?", (pokemon['name'],))
            self.assertEqual(cursor.fetchone(), (1, 0))

        # Delete the Pokémon
        delete_pokemon_database(pokemon['name'], DATABASE_PATH)

        # Confirm it was deleted
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Pokemon WHERE pokemon_name = ?", (pokemon['name'],))
            self.assertIsNone(cursor.fetchone())

            # Global stats should be zeroed again
            cursor.execute("SELECT global_encounters, global_shinies_found FROM General")
            self.assertEqual(cursor.fetchone(), (0, 0))

    #######################################################################################################################
    #######################################################################################################################

    def test_decrement_pokemon_shiny(self) -> None:

        """
        Tests that a shiny encounter is correctly decremented from a Pokémon and from global stats.

        Asserts:
            - Pokémon table shows correct shiny count after decrement.
            - Global shiny counter is updated correctly.

        Returns:
            None
        """

        pokemon = {'name': 'Squirtle'}
        playtime = 3.0

        # Add non-shiny encounter
        add_or_update_encounter({**pokemon, 'shiny': False}, playtime, DATABASE_PATH)

        # Add shiny encounter
        add_or_update_encounter({**pokemon, 'shiny': False}, playtime, DATABASE_PATH)
        add_or_update_encounter({**pokemon, 'shiny': True}, playtime, DATABASE_PATH)

        # Pre-check
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?", (pokemon['name'],))
            self.assertEqual(cursor.fetchone(), (2, 1))

            cursor.execute("SELECT global_encounters, global_shinies_found FROM General")
            self.assertEqual(cursor.fetchone(), (2, 1))

        # Perform decrement
        decrement_pokemon_shiny(pokemon['name'], DATABASE_PATH)

        # Post-check
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT encounters, shiny_encounters FROM Pokemon WHERE pokemon_name = ?", (pokemon['name'],))
            self.assertEqual(cursor.fetchone(), (2, 0))

            cursor.execute("SELECT global_encounters, global_shinies_found FROM General")
            self.assertEqual(cursor.fetchone(), (2, 0))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()