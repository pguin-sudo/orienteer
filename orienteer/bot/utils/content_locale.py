from enum import Enum


class Errors(Enum):
    no_user_id_with_ckey = 'Указанный пользователь не найден.'
    no_user_id_with_discord = 'Ваш аккаунт не привязан к игре.'
    no_playtime_info = 'Не удается найти данные о наигранном времени.'


class Results(Enum):
    no_bans_info = 'Не удается найти данные о банах, скорее всго их нет :).'
