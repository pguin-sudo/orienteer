from uuid import UUID

from loguru import logger

from orienteer.general.data.orienteer.services import sponsors
from orienteer.general.data.ss14.services import bans
from orienteer.general.utils.calculations import calculate_fine
from .base_product import Product
from datetime import datetime, timedelta, timezone


class ColoredNick(Product):
    id = 0
    name = 'Цветной ник в OOC чате на месяц'
    price_tag = '<:orienta:1250903370894671963>\'s'
    description = 'Внеси краски в свою жизнь и выделись на фоне остальных игроков. '
    'За 30 <:orienta:1250903370894671963>\'s укрась свой ник в ООС чате изменив его цвет на свой выбор.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926124941312/OOC.png'
    '?ex=666a9f8b&is=66694e0b&hm=97af81ca5481befdfe55eb31caa31871912158bc6896cf1572f666e3d5c78fcd&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '🖌'
    is_subscription = True
    cooldown = timedelta(days=31)

    async def calculate_price(user_id) -> int:
        return 29

    async def buy(user_id: UUID):
        logger.info(f'Покупка {__name__}')
        await sponsors.set_colored_nick(user_id, '87cefa')

    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {__name__}')
        await sponsors.set_colored_nick(user_id, None)


class GigachatAccess(Product):
    id = 1
    name = 'Доступ в гигачат на месяц'
    price_tag = '<:orienta:1250903370894671963>\'s'
    description = 'Прикоснись к немного более глубоким уровням взаимодействия администрации корпорации Ориента '
    'с участниками и стань членов чата спонсоров. Там ты сможешь общаться с директорами и другими '
    'членами проекта напрямую и в более неформальной обстановке. (а также посмотреть кукинг)'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350925860704268/GigaChat.png'
    '?ex=666a9f8b&is=66694e0b&hm=34ebe9a7aa56ebda9924aad7d6b427ed7a522b7b514ef77e59461cfb46ae9c3c&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '💬'
    is_subscription = True
    cooldown = timedelta(days=31)

    async def calculate_price(user_id) -> int:
        return 19

    async def buy(user_id: UUID):
        logger.info(f'Покупка {__name__}')
        await sponsors.set_sponsor_chat(user_id, True)
        await sponsors.set_activation(user_id, True)

    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {__name__}')
        await sponsors.set_sponsor_chat(user_id, False)
        # TODO: SOMETIMES HOLD ACTIVE


class PriorityQueue(Product):
    id = 2
    name = 'Приоритет в очереди на сервер на месяц'
    price_tag = '<:orienta:1250903370894671963>\'s'
    description = 'Если тебе (внезапно) неприятно долго ожидать в очереди чтобы зайти на сервер ты можешь купить '
    'этот товар и заходить на него быстрее других игроков.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '⏩'
    is_subscription = True
    cooldown = timedelta(days=31)

    async def calculate_price(user_id) -> int:
        return 19

    async def buy(user_id: UUID):
        logger.info(f'Покупка {__name__}')
        await sponsors.set_priority_queue(user_id, True)
        await sponsors.set_activation(user_id, True)

    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {__name__}')
        await sponsors.set_priority_queue(user_id, False)


class Orientalink(Product):
    id = 3
    name = 'Orientalink на месяц'
    price_tag = '<:orienta:1250903370894671963>\'s'
    description = 'Да, да, тот самый Orientalink с кучей раз\'а'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '📻'
    is_subscription = True
    cooldown = timedelta(days=31)

    async def calculate_price(user_id) -> int:
        return 19

    async def buy(user_id: UUID):
        logger.info(f'Покупка {__name__}')
        await sponsors.add_marking(user_id, 'Orientalink')
        await sponsors.set_activation(user_id, True)

    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {__name__}')
        await sponsors.remove_marking(user_id, 'Orientalink')


class BanAnnulment(Product):
    id = 4
    name = 'Аннулирование бана'
    price_tag = '<:orienta:1250903370894671963>\'s за ваш последний бан'
    description = 'По глупой случайности нарушил правила и очень раскаиваешься но администрация не согласилась '
    'удовлетворить твое обжалование? С этим товаром ты сможешь закончить свое наказание настолько раньше '
    'насколько вздумается.\n'
    '(Можно купить 1 раз в 2 недели, обнуляется только последний полученный бан)'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926418673695/Pardon.png'
    '?ex=666a9f8b&is=66694e0b&hm=fd912a41bc5d1bf027410abdb5dde27d0e365d719a64f967d8ca1914d4a8b9ce&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '🔓'
    is_subscription = False
    cooldown = timedelta(days=14)

    async def calculate_price(user_id) -> int:
        last_ban = await bans.get_last_ban(user_id)

        if last_ban is None:
            return 1

        expiration_time = last_ban['expiration_time']
        ban_time = last_ban['ban_time']

        if expiration_time is None:
            return 999

        return (await calculate_fine(expiration_time - ban_time))*2.5

    async def can_buy(user_id: UUID) -> bool:
        last_ban = await bans.get_last_ban(user_id)
        if last_ban is None or last_ban['expiration_time'] is None:
            return False
        else:
            return True

    async def buy(user_id: UUID):
        logger.info(f'Покупка {__name__}')
        await bans.pardon_last_ban(user_id)

    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {__name__}')
        raise NotImplementedError


def get_all_products() -> tuple[Product]:
    return (ColoredNick, GigachatAccess, PriorityQueue, Orientalink, BanAnnulment)
