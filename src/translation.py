"""This module contains the translation object and the translation function"""
import gettext
from database import SmokingDatabase


LANG = "en"


db = SmokingDatabase()


lang = db.get_language()
if lang:
    LANG = lang[0]


LOCALES_DIR = "locales" # /LC_MESSAGES/stop-smoke.mo


trans = gettext.translation('stop-smoke', localedir=LOCALES_DIR, languages=[LANG])


trans.install()


def _(text):
    """The translation function"""
    return trans.gettext(text)
