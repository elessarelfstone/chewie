import os
from dotenv import load_dotenv

load_dotenv()

# PROXY = {'proxy_url': 'http://213.153.63.119:8080'}
ADMIN_ID = os.getenv('ADMIN_ID')
TOKEN = os.getenv('TOKEN')
TEMP_DIR = os.getenv('TEMP_DIR')


DEFAULT_FONT = 'Arial'
CHARACTER_STYLE_TEMPALTE = {'font': DEFAULT_FONT, 'bold': False, 'italic': False, 'underline': False}

DB_HOST = os.getenv('DB_HOST')
DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASS = os.getenv('DB_PASS')
DB_BASE = os.getenv('DB_BASE')


