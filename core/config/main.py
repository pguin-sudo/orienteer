from dotenv import load_dotenv
import os

load_dotenv('.env')


class Debug:
    MODE = os.getenv('DEBUG_MODE')


class Bot:
    TOKEN = os.getenv('BOT_TOKEN')
    NAME = os.getenv('BOT_NAME')
    ID = os.getenv('BOT_ID')
    PREFIX = os.getenv('BOT_PREFIX')


class Webhooks:
    ERRORS = os.getenv('WEBHOOKS_ERRORS')
    BANS = os.getenv('WEBHOOKS_BANS')
    ROLEBANS = os.getenv('WEBHOOKS_ROLEBANS')


class OAuth2:
    API_ENDPOINT = os.getenv('OAUTH2_ENDPOINT')
    CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID')
    CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('OAUTH2_REDIRECT_URI')
    API_KEY = os.getenv('OAUTH2_API_KEY')


class Cache:
    SPONSORS_DATA = os.getenv('CACHE_SPONSORS_DATA')
    BANS_LAST_ID = os.getenv('CACHE_BANS_LAST_ID')
    ROLEBANS_LAST_ID = os.getenv('CACHE_ROLEBANS_LAST_ID')


class Postgres:
    HOST = os.getenv('POSTGRES_HOST')
    PORT = os.getenv('POSTGRES_PORT')
    DBNAME = os.getenv('POSTGRES_DBNAME')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')


class Private:
    ADMINS = os.getenv('PRIVATE_ADMINS')


class Roles:
    PASSENGER = os.getenv('ROLES_PASSENGER')
    YOUTUBER = os.getenv('ROLES_YOUTUBER')
