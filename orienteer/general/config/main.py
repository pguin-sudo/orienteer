import os

from dotenv import load_dotenv

load_dotenv(".env")

# Debug settings
DEBUG_MODE = False
DEBUG_DB_ECHO = False

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = "Orienteer"
BOT_ID = os.getenv("BOT_ID")
BOT_PREFIX = "/"

# Webhooks
WEBHOOKS_LOGS = {
    "api": os.getenv("WEBHOOKS_LOGS_API"),
    "bot": os.getenv("WEBHOOKS_LOGS_BOT"),
    "checker": os.getenv("WEBHOOKS_LOGS_CHECKER"),
}
WEBHOOKS_BANS = os.getenv("WEBHOOKS_BANS")
WEBHOOKS_SEASONS = os.getenv("WEBHOOKS_SEASONS")

# OAuth2 settings
AUTH_API_ENDPOINT = "https://discord.com/api/v10"
AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")
AUTH_REDIRECT_URI = "http://amadis.orientacorp.ru:8080/api/auth/redirect"
AUTH_API_KEY = os.getenv("AUTH_API_KEY")

# Postgres settings for SS14
POSTGRES_SS14_HOST = os.getenv("POSTGRES_SS14_HOST")
POSTGRES_SS14_PORT = os.getenv("POSTGRES_SS14_PORT")
POSTGRES_SS14_DBNAME = os.getenv("POSTGRES_SS14_DBNAME")
POSTGRES_SS14_USER = os.getenv("POSTGRES_SS14_USER")
POSTGRES_SS14_PASSWORD = os.getenv("POSTGRES_SS14_PASSWORD")

# Postgres settings for Orienteer
POSTGRES_ORIENTEER_HOST = os.getenv("POSTGRES_ORIENTEER_HOST")
POSTGRES_ORIENTEER_PORT = os.getenv("POSTGRES_ORIENTEER_PORT")
POSTGRES_ORIENTEER_DBNAME = os.getenv("POSTGRES_ORIENTEER_DBNAME")
POSTGRES_ORIENTEER_USER = os.getenv("POSTGRES_ORIENTEER_USER")
POSTGRES_ORIENTEER_PASSWORD = os.getenv("POSTGRES_ORIENTEER_PASSWORD")

# Tokens
TOKEN_PLAYTIME = os.getenv("TOKEN_PLAYTIME")

# Users
USERS_OWNERS = set(map(int, os.getenv("USERS_OWNERS", "").split(",")))

# Roles
ROLES_PASSENGER = 1249746549937016945
ROLES_YOUTUBER = 1246884539142246470
ROLES_GIGACHAT = 1246886565599514644
ROLES_BOOSTER = 1278436102323044502
ROLES_ELDERLING = 1247181537905082480

# Emoji
CURRENCY_SIGN = "<:orienta:1278806225773133915>"

# Seasons
SEASON_MESSAGE_ID = 1268478529700368456

# Orientiks
ORIENTIKS_MARGIN = 0.1
ORIENTIKS_PRICE_COEFFICIENT = 2
