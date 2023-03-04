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

def _(text):
    return trans.gettext(text)
