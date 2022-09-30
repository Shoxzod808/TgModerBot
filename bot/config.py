import os
import django
import sys

PACKAGE_PARENT = '..'
APP_DIR = os.path.join(PACKAGE_PARENT, 'app')
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))
    )
)
APP_DIR_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, APP_DIR))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(APP_DIR_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

TOKEN = '2128617922:AAGrzZOzO2lGT4eXUlSiHxYkGNB1OYeAqOk'
CHAT_ID = 2128617922
CURRENT_URL = 'TopMuzicBot'