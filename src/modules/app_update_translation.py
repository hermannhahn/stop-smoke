"""This module contains the translation object and the translation function"""
import gettext
from db.database import SmokingDatabase


LANG = "en"


db = SmokingDatabase()


lang = db.get_language()
if lang:
    LANG = lang[0]


LOCALES_DIR = "locales"


trans = gettext.translation('update', localedir=LOCALES_DIR, languages=[LANG])


trans.install()


def _(text):
    """The translation function"""
    return trans.gettext(text)
