from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from loguru import logger


@dataclass
class Product:
    id: int
    name: str = 'Продукт'
    price: int = '12'
    price_tag: str = ' ориентиков за неделю'
    description: str = 'Описани'
    image_url: str = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926124941312/OOC.png'
    '?ex=666a9f8b&is=66694e0b&hm=97af81ca5481befdfe55eb31caa31871912158bc6896cf1572f666e3d5c78fcd&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji: str = '🖌'
    is_subscription: bool = False
    cooldown: timedelta | None = timedelta(days=31)

    async def can_buy(user_id: UUID) -> bool:
        return True

    async def buy(user_id: UUID):
        logger.info(f'Покупка {__name__}')

    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {__name__}')
