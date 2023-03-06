import gettext
from database import SmokingDatabase

# Set default language
LANG = "en"

# Create a database object
db = SmokingDatabase()

# Get the language from the database, check if it's not None and set it
lang = db.get_language()
if lang:
    LANG = lang[0]

# Set the path to the translation files
LOCALES_DIR = "locales" # /LC_MESSAGES/stop-smoke.mo

# Create a translation object
trans = gettext.translation('stop-smoke', localedir=LOCALES_DIR, languages=[LANG])

# Install the translation object
trans.install()

# Create a function to translate text
def _(text):
    return trans.gettext(text)
