from datetime import timedelta
from uuid import UUID

from loguru import logger

from orienteer.general.config import CURRENCY_SIGN, ROLES_BOOSTER
from orienteer.general.data.orienteer.services import orientiks
from orienteer.general.data.orienteer.services.discord_auth import get_discord_user_id_by_user_id
from orienteer.general.data.products.products.abstract import AbstractProduct
from orienteer.general.data.ss14.services import whitelist
from orienteer.general.utils import discord


class Orientiks10(AbstractProduct):
    id = 100
    name = '10 ориентиков'
    price_tag = CURRENCY_SIGN
    description = 'Спонсорские 10 ориентиков на всегда.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    boosty = True
    emoji = '💳'
    is_subscription = False

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return False

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {Orientiks10.name}')
        await orientiks.add_orientiks_from_sponsorship(user_id, 10)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {Orientiks10.name}')
        await orientiks.add_orientiks_from_sponsorship(user_id, -10)


class Whitelist(AbstractProduct):
    id = 101
    name = 'Вайтлист'
    price_tag = CURRENCY_SIGN
    description = 'Спонсорский вайтлист'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    boosty = True
    emoji = '💳'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return False

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {Orientiks10.name}')
        await whitelist.add_to_whitelist(user_id)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {Orientiks10.name}')
        await whitelist.delete_from_whitelist(user_id)


class BoostyRole(AbstractProduct):
    id = 102
    name = 'Роль бустера'
    price_tag = CURRENCY_SIGN
    description = 'Спонсорская роль бустера корпорации.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    boosty = True
    emoji = '👾'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return False

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {BoostyRole.name}')
        await discord.set_role(await get_discord_user_id_by_user_id(user_id=user_id), ROLES_BOOSTER, False)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {BoostyRole.name}')
        await discord.set_role(await get_discord_user_id_by_user_id(user_id=user_id), ROLES_BOOSTER, True)


class AllRoles(AbstractProduct):
    id = 103
    name = 'Все роли'
    price_tag = CURRENCY_SIGN
    description = 'Спонсорская подписка на все роли.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    boosty = True
    emoji = '🍥'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return False

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {BoostyRole.name}')
        logger.error('Бля, мне лень делать имплементацию выдачи времени')

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {BoostyRole.name}')
        logger.error('Бля, мне лень делать имплементацию выдачи времени')


class NewItems(AbstractProduct):
    id = 104
    name = 'Уникальный предмет'
    price_tag = CURRENCY_SIGN
    description = 'Спонсорская подписка на все роли.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    boosty = True
    emoji = '🍥'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return False

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {BoostyRole.name}')
        logger.error('Бля, мне лень делать имплементацию выдачи времени')

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {BoostyRole.name}')
        logger.error('Бля, мне лень делать имплементацию выдачи времени')
