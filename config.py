import os
from pathlib import Path
import logging
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

BACKEND = "Zulip"
BOT_EXTRA_BACKEND_DIR = str(BASE_DIR / 'backend-zulip')

BOT_DATA_DIR = str(BASE_DIR / "data")
BOT_EXTRA_PLUGIN_DIR = str(BASE_DIR / "plugins")

BOT_LOG_FILE = None  # Console-only
BOT_LOG_LEVEL = logging.INFO

BOT_IDENTITY = { 
  'email': 'garv-bot@magistrate.zulipchat.com',
  'key': os.environ['ZULIP_BOT_KEY'],
  'site': 'https://magistrate.zulipchat.com'
}

BOT_ADMINS = (
    "harry@getmagistrate.com",
) 

CHATROOM_PRESENCE = ()
BOT_PREFIX = '!'

HIDE_RESTRICTED_COMMANDS = True