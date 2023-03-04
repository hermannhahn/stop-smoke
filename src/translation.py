import gettext
import locale

# Get the system language
LANG = locale.getlocale()[0]
# If the system language is not defined, use the default language
if not LANG:
    LANG = 'en_US'

# Set the path to the translation files
LOCALES_DIR = "locales" # /LC_MESSAGES/stop-smoke.mo
 
# Create a translation object
trans = gettext.translation('stop-smoke', localedir=LOCALES_DIR, languages=[LANG])

# Install the translation object
trans.install()

# Create a function to translate text
def _(text):
    return trans.gettext(text)
