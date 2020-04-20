import os
from dotenv import load_dotenv
from os.path import expanduser

load_dotenv()

ADMIN_ID = os.getenv('ADMIN_ID')
TOKEN = os.getenv('TOKEN')
TEMP_DIR = os.path.join(os.path.expanduser('~'), 'temp')


DEFAULT_FONT = 'Arial'
CHARACTER_STYLE_TEMPALTE = {'font': DEFAULT_FONT, 'bold': False, 'italic': False, 'underline': False}

DB_FPATH = os.path.join(expanduser("~"), 'db', 'chewie.db')

JOBS_PICKLE = 'job_tuples.pickle'
JOBS_PICKLE_PATH = os.path.join(TEMP_DIR, JOBS_PICKLE)

# WARNING: This information may change in future versions (changes are planned)
JOB_DATA = ('callback', 'interval', 'repeat', 'context', 'days', 'name', 'tzinfo')
JOB_STATE = ('_remove', '_enabled')
