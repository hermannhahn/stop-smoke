"""
Title: App translation module
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: This module contains the translation object and the translation function
To use the translation function, import the module and use the function like this:
e.g.
from modules.app_translation import _
print(_("Hello World"))
"""
import gettext
from db.database import SmokingDatabase # pylint: disable=import-error,no-name-in-module

# Set default language
LANG = "en"

# Set locales directory
LOCALES_DIR = "locales"

# Get database object
db = SmokingDatabase()

# Get language from database
lang = db.get_language()
if lang:
    LANG = lang[0]

# Set translation object
trans = gettext.translation('stopsmoke', localedir=LOCALES_DIR, languages=[LANG])

# Install translation object
trans.install()


def _(text):
    """The translation function"""
    return trans.gettext(text)
