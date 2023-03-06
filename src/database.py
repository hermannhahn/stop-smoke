import sqlite3

# Class to manage the database
class SmokingDatabase:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect('smoking.db')
        self.c = self.conn.cursor()

        # Create the table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS smoking (
                            last_smoke INTEGER,
                            wait_time INTEGER,
                            first_run BOOLEAN,
                            language TEXT
                            )''')
        # Commit the changes
        self.conn.commit()

    # Get the data from the database
    def get_data(self):
        self.c.execute("SELECT * FROM smoking")
        data = self.c.fetchone()
        # If there is no data, insert the data
        if not data:
            self.c.execute("INSERT INTO smoking VALUES (?,?,?,?)", (None, None, True, "en"))
            self.conn.commit()
            # Get the data from the database
            self.c.execute("SELECT * FROM smoking")
            data = self.c.fetchone()
        return data
    
    # Update the data in the database
    def update_data(self, last_smoke, wait_time):
        self.c.execute("UPDATE smoking SET last_smoke = ?, wait_time = ?, first_run = ?", (last_smoke, wait_time, False))
        self.conn.commit()

    # Get the language from the database
    def get_language(self):
        self.c.execute("SELECT language FROM smoking")
        language = self.c.fetchone()
        return language

    # Return the language name from the database
    def get_language_name(self):
        self.c.execute("SELECT language FROM smoking")
        language = self.c.fetchone()[0]
        if language == "en":
            return _("English")
        elif language == "fr":
            return _("French")
        elif language == "de":
            return _("German")
        elif language == "it":
            return _("Italian")
        elif language == "pt_BR":
            return _("Portuguese")
        elif language == "ru":
            return _("Russian")
        elif language == "es":
            return _("Spanish")

    # Update the language in the database
    def update_language(self, language):
        self.c.execute("UPDATE smoking SET language = ?", (language,))
        self.conn.commit()

    # First run check
    def first_run(self):
        # Get the data from the database
        data = self.get_data()
        # If the data is not defined, insert the data
        if not data or data[2] == True:
            return True