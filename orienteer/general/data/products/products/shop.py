from datetime import timedelta
from uuid import UUID

from loguru import logger

from orienteer.general.config import CURRENCY_SIGN
from orienteer.general.data.orienteer.services import sponsors, orientiks
from orienteer.general.data.ss14.services import bans
from orienteer.general.utils.calculations import calculate_fine
from .abstract import AbstractProduct


class ColoredNick(AbstractProduct):
    id = 0
    name = 'Цветной ник в OOC чате на месяц'
    price_tag = CURRENCY_SIGN
    description = f'Внеси краски в свою жизнь и выделись на фоне остальных игроков. '
    'За 30 {CURRENCY_SIGN} укрась свой ник в ООС чате изменив его цвет на свой выбор.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926124941312/OOC.png'
    '?ex=666a9f8b&is=66694e0b&hm=97af81ca5481befdfe55eb31caa31871912158bc6896cf1572f666e3d5c78fcd&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '🖌'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return 29

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        sponsor = await sponsors.get_sponsor(user_id)
        return sponsor is None or sponsor.ooc_color is None

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {ColoredNick.name}')
        await sponsors.set_colored_nick(user_id, '87cefa')

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {ColoredNick.name}')
        await sponsors.set_colored_nick(user_id, None)


class GigachatAccess(AbstractProduct):
    id = 1
    name = 'Доступ в гигачат на месяц'
    price_tag = CURRENCY_SIGN
    description = 'Прикоснись к немного более глубоким уровням взаимодействия администрации корпорации Ориента '
    'с участниками и стань членов чата спонсоров. Там ты сможешь общаться (в том числе, обсуждая рецепты блюд) '
    'с директорами и другими членами проекта напрямую и в более неформальной обстановке.'

    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350925860704268/GigaChat.png'
    '?ex=666a9f8b&is=66694e0b&hm=34ebe9a7aa56ebda9924aad7d6b427ed7a522b7b514ef77e59461cfb46ae9c3c&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '💬'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return 19

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        sponsor = await sponsors.get_sponsor(user_id)
        return sponsor is None or sponsor.have_sponsor_chat is None or not sponsor.have_sponsor_chat

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {GigachatAccess.name}')
        await sponsors.set_sponsor_chat(user_id, True)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {GigachatAccess.name}')
        await sponsors.set_sponsor_chat(user_id, False)


class PriorityQueue(AbstractProduct):
    id = 2
    name = 'Приоритет в очереди на сервер на месяц'
    price_tag = CURRENCY_SIGN
    description = 'Если тебе (внезапно) неприятно долго ожидать в очереди чтобы зайти на сервер ты можешь купить '
    'этот товар и заходить на него быстрее других игроков.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '⏩'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return 19

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        sponsor = await sponsors.get_sponsor(user_id)
        return sponsor is None or sponsor.have_priority_join is None or not sponsor.have_priority_join

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {PriorityQueue.name}')
        await sponsors.set_priority_join(user_id, True)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {PriorityQueue.name}')
        await sponsors.set_priority_join(user_id, False)


class Orientalink(AbstractProduct):
    id = 3
    name = 'Orientalink на месяц'
    price_tag = CURRENCY_SIGN
    description = 'Да, да, тот самый Orientalink с кучей различных плюшек.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '📻'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return 19

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        sponsor = await sponsors.get_sponsor(user_id)
        return sponsor is None or 'Orientalink' not in sponsor.allowed_markings

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {Orientalink.name}')
        await sponsors.add_marking(user_id, 'Orientalink')

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {Orientalink.name}')
        await sponsors.remove_marking(user_id, 'Orientalink')


class BanAnnulment(AbstractProduct):
    id = 4
    name = 'Аннулирование бана'
    price_tag = f'{CURRENCY_SIGN} за ваш последний бан'
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

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        last_ban = await bans.get_last_ban(user_id)

        if last_ban is None:
            return 1

        expiration_time = last_ban['expiration_time']
        ban_time = last_ban['ban_time']

        if expiration_time is None:
            return None

        return int((calculate_fine(expiration_time - ban_time)) * 2.5)

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        last_ban = await bans.get_last_ban(user_id)
        if last_ban is None or last_ban['expiration_time'] is None:
            return False
        else:
            return True

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {BanAnnulment.name}')
        await bans.pardon_last_ban(user_id)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {BanAnnulment.name}')
        raise NotImplementedError


class SevenNewSlots(AbstractProduct):
    id = 5
    name = '7 слотов на месяц'
    price_tag = CURRENCY_SIGN
    description = '7 дополнительных слотов для персонажей в меню персонализации.'
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '🎰'
    is_subscription = True
    cooldown = timedelta(days=31)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        sponsor = await sponsors.get_sponsor(user_id)
        return sponsor is None or sponsor.extra_slots == 0

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {SevenNewSlots.name}')
        await sponsors.add_extra_clots(user_id, 7)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {SevenNewSlots.name}')
        await sponsors.add_extra_clots(user_id, -7)


class SevenOrientiks(AbstractProduct):
    id = 6
    name = '21 ориентик на 24 часа'
    price_tag = CURRENCY_SIGN
    description = ('Да, ты всё правильно понял это 21 ориентик на 24 часа за 7 ориентиков. В чем подвох? Подвоха нет. '
                   'Это просто 21 ориентик на 24 часа за 7 ориентиков.')
    image_url = 'https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
    '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
    '&format=webp&quality=lossless&width=725&height=671'
    emoji = '💳'
    is_subscription = True
    cooldown = timedelta(days=1)

    @staticmethod
    async def calculate_price(user_id: UUID) -> int | None:
        return None

    @staticmethod
    async def can_buy(user_id: UUID) -> bool:
        return True

    @staticmethod
    async def buy(user_id: UUID):
        logger.info(f'Покупка {SevenOrientiks.name}')
        await orientiks.add_orientiks_from_sponsorship(user_id, 21)

    @staticmethod
    async def retrieve(user_id: UUID):
        logger.info(f'Возврат {SevenOrientiks.name}')
        await orientiks.add_orientiks_from_sponsorship(user_id, -21)
