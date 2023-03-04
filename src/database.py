import sqlite3

class SmokingDatabase:
    def __init__(self):
        # Conecta ao banco de dados
        self.conn = sqlite3.connect('smoking.db')
        self.c = self.conn.cursor()

        # Cria a tabela se ela não existir
        self.c.execute('''CREATE TABLE IF NOT EXISTS smoking (
                            last_smoke INTEGER,
                            wait_time INTEGER
                            )''')
        self.conn.commit()

    def get_data(self):
        # Obtém o intervalo e a última vez que fumou do banco de dados
        self.c.execute("SELECT * FROM smoking")
        data = self.c.fetchone()
        return data

    def update_data(self, last_smoke, wait_time):
        # Atualiza o intervalo e a última vez que fumou no banco de dados
        self.c.execute("UPDATE smoking SET last_smoke = ?, wait_time = ?", (last_smoke, wait_time))
        self.conn.commit()

    def insert_data(self, last_smoke, wait_time):
        # Insere intervalo e a última vez que fumou no banco de dados
        self.c.execute("INSERT INTO smoking VALUES (?, ?)", (last_smoke, wait_time))
        self.conn.commit()
