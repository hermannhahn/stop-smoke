"""Database module"""
import sqlite3


class SmokingDatabase:
    """Class to manage the database"""

    def __init__(self):
        """Connect to the database and create the table if it doesn't exist"""
        self.conn = sqlite3.connect('smoking.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS smoking (
                            last_smoke INTEGER,
                            wait_time INTEGER,
                            first_run BOOLEAN,
                            language TEXT
                            )''')

        self.conn.commit()


    def get_data(self):
        """Get the data from the database"""
        self.cursor.execute("SELECT * FROM smoking")
        data = self.cursor.fetchone()

        if not data:
            self.cursor.execute("INSERT INTO smoking VALUES (?,?,?,?)", (None, None, True, "en"))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM smoking")
            data = self.cursor.fetchone()

        return data


    def update_data(self, last_smoke, wait_time):
        """Update the data in the database"""
        self.cursor.execute("UPDATE smoking SET last_smoke = ?", (last_smoke,))
        self.cursor.execute("UPDATE smoking SET wait_time = ?", (wait_time,))
        self.cursor.execute("UPDATE smoking SET first_run = ?", (False,))
        self.conn.commit()


    def get_language(self):
        """Get the language from the database"""
        self.cursor.execute("SELECT language FROM smoking")
        language = self.cursor.fetchone()
        return language


    def get_language_name(self):
        """Return the language name from the database"""
        self.cursor.execute("SELECT language FROM smoking")
        language = self.cursor.fetchone()[0]

        language_name_list = {
            "en": _("English"),
            "fr": _("French"),
            "de": _("German"),
            "it": _("Italian"),
            "pt_BR": _("Portuguese"),
            "ru": _("Russian"),
            "es": _("Spanish")
        }

        return language_name_list[language]


    def update_language(self, language):
        """Update the language in the database"""
        self.cursor.execute("UPDATE smoking SET language = ?", (language,))
        self.conn.commit()


    def first_run(self):
        """Check if it's the first run"""
        data = self.get_data()

        if not data or data[2] is True:
            return True
        return False
