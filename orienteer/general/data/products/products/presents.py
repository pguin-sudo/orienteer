from datetime import timedelta
from uuid import UUID

from loguru import logger

from orienteer.general.config import CURRENCY_SIGN
from orienteer.general.data.orienteer.services import transactions
from orienteer.general.data.products.products.abstract import AbstractProduct


class Orientiks33(AbstractProduct):
    id = 200
    name = '33 ориентика'
    price_tag = CURRENCY_SIGN
    description = '33 ориентика на всегда для победителя.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    boosty = False
    emoji = '🪙'
    is_subscription = False
    cooldown = timedelta()

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return False

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {Orientiks33.name}')
        await transactions.add_orientiks_from_other(user_id, 33, "Orientiks 33")

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {Orientiks33.name}')
        await transactions.add_orientiks_from_other(user_id, -33, "Orientiks 33")


all_: tuple[AbstractProduct] = (Orientiks33,)  # noqa
