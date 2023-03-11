"""
Title: SQLite Database module
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: This module contains the database class
"""
import sqlite3


class SmokingDatabase:
    """Class to manage the database"""

    def __init__(self):
        """Initialize the database"""

        # Connect to the database
        self.conn = sqlite3.connect('stopsmoking.db')
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS smoking (
                            last_smoke INTEGER,
                            wait_time INTEGER,
                            first_run BOOLEAN,
                            language TEXT
                            )''')

        # Commit the changes
        self.conn.commit()


    def get_data(self):
        """Get the data from the database"""

        # Get the data
        self.cursor.execute("SELECT * FROM smoking")
        data = self.cursor.fetchone()

        # If there is no data, create a new entry
        if not data:
            self.cursor.execute("INSERT INTO smoking VALUES (?,?,?,?)", (0, 90 * 60, True, "en"))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM smoking")
            data = self.cursor.fetchone()

        # Return the data
        return data


    def update_data(self, last_smoke, wait_time):
        """Update the data in the database"""

        # Update the data
        self.cursor.execute("UPDATE smoking SET last_smoke = ?", (last_smoke,))
        self.cursor.execute("UPDATE smoking SET wait_time = ?", (wait_time,))
        self.cursor.execute("UPDATE smoking SET first_run = ?", (False,))

        # Commit the changes
        self.conn.commit()


    def get_language(self):
        """Get the language from the database"""

        # Get the language
        self.cursor.execute("SELECT language FROM smoking")
        language = self.cursor.fetchone()

        # Return the language
        return language


    def get_language_name(self, language):
        """Return the language name from the database"""

        # Create a dictionary with the native language names
        language_name_list = {
            "en": ("English"),
            "fr": ("Francés"),
            "de": ("Deutsch"),
            "it": ("Italiano"),
            "pt_BR": ("Portugues"),
            "es": ("Castelhano"),
            "ru": ("русский язык")
        }

        # Return the language name
        return language_name_list[language]


    def update_language(self, language):
        """Update the language in the database"""

        # Update the language
        self.cursor.execute("UPDATE smoking SET language = ?", (language,))
        self.conn.commit()


    def first_run(self):
        """Check if it's the first run"""

        # Get the data
        data = self.get_data()

        # Check if it's the first run and return the result
        if not data or data[2] is True:
            return True
        return False
