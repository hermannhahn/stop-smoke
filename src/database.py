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
                            wait_time INTEGER
                            )''')
        self.conn.commit()

    # Get the data from the database
    def get_data(self):
        self.c.execute("SELECT * FROM smoking")
        data = self.c.fetchone()
        return data

    # Update the data in the database
    def update_data(self, last_smoke, wait_time):
        self.c.execute("UPDATE smoking SET last_smoke = ?, wait_time = ?", (last_smoke, wait_time))
        self.conn.commit()

    # Insert the data in the database
    def insert_data(self, last_smoke, wait_time):
        self.c.execute("INSERT INTO smoking VALUES (?, ?)", (last_smoke, wait_time))
        self.conn.commit()
