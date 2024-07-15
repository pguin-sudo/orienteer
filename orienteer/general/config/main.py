import os
from dotenv import load_dotenv


load_dotenv('.env')

# Debug settings
DEBUG_MODE = False

# Bot settings
BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_NAME = 'Orienteer'
BOT_ID = os.environ.get('BOT_ID')
BOT_PREFIX = '/'

# Webhooks
WEBHOOKS_ERRORS = os.environ.get('WEBHOOKS_ERRORS')
WEBHOOKS_BANS = os.environ.get('WEBHOOKS_BANS')
WEBHOOKS_ROLEBANS = os.environ.get('WEBHOOKS_ROLEBANS')

# OAuth2 settings
AUTH_API_ENDPOINT = 'https://discord.com/api/v10'
AUTH_CLIENT_SECRET = os.environ.get('AUTH_CLIENT_SECRET')
AUTH_REDIRECT_URI = 'http://amadis.orientacorp.ru:8080/api/auth/redirect'
AUTH_API_KEY = os.environ.get('AUTH_API_KEY')

# Postgres settings
POSTGRES_SS14_HOST = os.environ.get('POSTGRES_SS14_HOST')
POSTGRES_SS14_PORT = os.environ.get('POSTGRES_SS14_PORT')
POSTGRES_SS14_DBNAME = os.environ.get('POSTGRES_SS14_DBNAME')
POSTGRES_SS14_USER = os.environ.get('POSTGRES_SS14_USER')
POSTGRES_SS14_PASSWORD = os.environ.get('POSTGRES_SS14_PASSWORD')

POSTGRES_ORIENTEER_HOST = os.environ.get('POSTGRES_ORIENTEER_HOST')
POSTGRES_ORIENTEER_PORT = os.environ.get('POSTGRES_ORIENTEER_PORT')
POSTGRES_ORIENTEER_DBNAME = os.environ.get('POSTGRES_ORIENTEER_DBNAME')
POSTGRES_ORIENTEER_USER = os.environ.get('POSTGRES_ORIENTEER_USER')
POSTGRES_ORIENTEER_PASSWORD = os.environ.get('POSTGRES_ORIENTEER_PASSWORD')

# Users
USERS_OWNERS = set(map(int, os.environ.get('USERS_OWNERS').split(',')))

# Roles
ROLES_PASSENGER = 1249746549937016945
ROLES_YOUTUBER = 1246884539142246470
