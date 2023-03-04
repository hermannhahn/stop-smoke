import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import sqlite3
import os
import gettext
import locale

# Define a linguagem do sistema baseado na configuração do sistema
LANG = locale.getlocale()[0]
if not LANG:
    LANG = 'pt_BR'

# Define o diretório de tradução
LOCALES_DIR = "locales"

# Define a tradução
trans = gettext.translation('stop-smoke', localedir=LOCALES_DIR, languages=[LANG])

# Instala a tradução
trans.install()


# Classe principal do aplicativo
class StopSmokingApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # Define o título da janela na linguagem do sistema
        self.master.title(gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Stop Smoking"))
        # Define o ícone da janela
        self.master.iconbitmap(os.path.abspath("icon.ico"))
        # Define o tamanho da janela
        self.master.geometry("350x120")
        # Define o comportamento ao fechar a janela
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        
        self.pack()

        # Define ícone do aplicativo
        self.icon_path = os.path.abspath("icon.ico")

        # Conecta ao banco de dados
        self.conn = sqlite3.connect('smoking.db')
        self.c = self.conn.cursor()

        # Cria a tabela se ela não existir
        self.c.execute('''CREATE TABLE IF NOT EXISTS smoking (
                            last_smoke INTEGER,
                            wait_time INTEGER
                            )''')
        self.conn.commit()

        # Obtém o intervalo e a última vez que fumou do banco de dados
        self.c.execute("SELECT * FROM smoking")
        data = self.c.fetchone()
        if data is None:
            # Se não houver dados no banco de dados, pergunte ao usuário com uma janela
            # gráfica qual será o intervalo incial e inicializa o intervalo de acordo
            # com a resposta e a data da última vez que fumou como a hora atual
            self.wait_time = int(simpledialog.askinteger(gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Stop Smoking"), gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("How many minutes do you want to wait between smokes?"), parent=self.master)) * 60
            self.last_smoke = time.time() - self.wait_time
            self.c.execute("INSERT INTO smoking VALUES (?, ?)", (self.last_smoke, self.wait_time))
            self.conn.commit()
        else:
            # Se houver dados no banco de dados, usa os valores armazenados
            self.last_smoke = data[0]
            self.wait_time = data[1]

        self.create_widgets()

    def create_widgets(self):
        # Cria um rótulo para exibir o tempo restante até poder fumar novamente
        self.time_left_label = tk.Label(self)
        self.time_left_label["text"] = gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Time left: {} minutes").format(int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)
        self.time_left_label.pack(pady=15)

        # Cria um botão para registrar quando fumar
        self.smoke_button = tk.Button(self)
        self.smoke_button["text"] = gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Smoke")
        self.smoke_button["state"] = "normal"
        self.smoke_button["command"] = self.smoke
        self.smoke_button.pack(pady=5)

        # Atualiza o rótulo de tempo restante se o tempo restante for maior que zero
        self.update_screen()

    def get_time_left(self):
        # Calcula o tempo restante em minutos até poder fumar novamente
        time_left = int(max(0, self.last_smoke + self.wait_time - time.time()) / 60)
        return time_left
    
    def smoke(self):
        # Registra a data da última vez que fumou como a hora atual
        self.last_smoke = time.time()

        # Atualiza o intervalo e a última vez que fumou no banco de dados
        self.c.execute("UPDATE smoking SET last_smoke = ?, wait_time = ?", (self.last_smoke, self.wait_time))
        self.conn.commit()

        # Atualiza o rótulo de tempo restante se o tempo restante for maior que zero
        self.update_screen()

    # Atualiza o rótulo de tempo restante e botão de fumar
    def update_screen(self):

        if self.get_time_left() > 0:
            # Atualize o titulo da janela
            self.master.title(gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Stop Smoking"))
            # Atualiza o estado do botão de fumar
            self.smoke_button["state"] = "disabled"
            # Exibe o tempo restante na linguagem do sistema
            self.time_left_label["text"] = gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Time left: {} minutes").format(int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)
        else:
            # Atualize o titulo da janela
            self.master.title(gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("Free to Smoke"))
            # Atualiza o estado do botão de fumar
            self.smoke_button["state"] = "normal"
            # Exibe a mensagem de que você pode fumar novamente na linguagem do sistema
            self.time_left_label["text"] = gettext.translation("stop-smoke", localedir=LOCALES_DIR, languages=[LANG]).gettext("You can smoke again")

        # chamada para atualizar a tela novamente após 1 segundo
        self.after(1000, self.update_screen)

    def quit(self):
        # Encerra a conexão com o banco de dados antes de sair do aplicativo
        self.conn.close()
        self.master.destroy()

root = tk.Tk()
app = StopSmokingApp(master=root)
app.mainloop()
