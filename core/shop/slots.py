from core.shop import functions


class Product:
    def __init__(self, name: str, price: int, price_tag: str, description: str, image_url: str, emoji: str, func):
        self.name = name
        self.price = price
        self.price_tag = price_tag
        self.description = description
        self.image_url = image_url
        self.emoji = emoji
        self.func = func


colored_nick = Product(
    name='Цветной ник в OOC чате на 1 месяц',
    price=29,
    price_tag='<:orienta:1250903370894671963>\'s',
    description='Внеси краски в свою жизнь и выделись на фоне остальных игроков. '
                'За 30 <:orienta:1250903370894671963>\'s укрась свой ник в ООС чате, изменив его цвет на свой выбор.',
    image_url='https://media.discordapp.net/attachments/1162830763390140548/1250350926124941312/OOC.png'
              '?ex=666a9f8b&is=66694e0b&hm=97af81ca5481befdfe55eb31caa31871912158bc6896cf1572f666e3d5c78fcd&='
              '&format=webp&quality=lossless&width=725&height=671',
    emoji='🖌',
    func=functions.colored_nick
)

gigachat_access = Product(
    name='Доступ в гигачат на 1 месяц',
    price=19,
    price_tag='<:orienta:1250903370894671963>\'s',
    description='Прикоснись к немного более глубоким уровням взаимодействия администрации корпорации Ориента '
                'с участниками и стань членов чата спонсоров. Там ты сможешь общаться с директорами и другими '
                'членами проекта напрямую и в более неформальной обстановке.',
    image_url='https://media.discordapp.net/attachments/1162830763390140548/1250350925860704268/GigaChat.png'
              '?ex=666a9f8b&is=66694e0b&hm=34ebe9a7aa56ebda9924aad7d6b427ed7a522b7b514ef77e59461cfb46ae9c3c&='
              '&format=webp&quality=lossless&width=725&height=671',
    emoji='💬',
    func=functions.gigachat_access
)

ban_annulment = Product(
    name='Аннулирование бана',
    price=12,
    price_tag='<:orienta:1250903370894671963>\'s за 1 день бана',
    description='По глупой случайности нарушил правила и очень раскаиваешься, но администрация не согласилась '
                'удовлетворить твое обжалование? С этим товаром ты сможешь закончить свое наказание настолько раньше, '
                'насколько вздумается.',
    image_url='https://media.discordapp.net/attachments/1162830763390140548/1250350926418673695/Pardon.png'
              '?ex=666a9f8b&is=66694e0b&hm=fd912a41bc5d1bf027410abdb5dde27d0e365d719a64f967d8ca1914d4a8b9ce&='
              '&format=webp&quality=lossless&width=725&height=671',
    emoji='🔓',
    func=functions.ban_annulment
)

priority_queue = Product(
    name='Приоритет в очереди на сервер',
    price=19,
    price_tag='<:orienta:1250903370894671963>\'s',
    description='Если тебе (внезапно) неприятно долго ожидать в очереди, чтобы зайти на сервер, ты можешь купить '
                'этот товар и заходить на него быстрее других игроков.',
    image_url='https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
              '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
              '&format=webp&quality=lossless&width=725&height=671',
    emoji='⏩',
    func=functions.priority_queue
)

orienta = Product(
    name='Orientalink',
    price=19,
    price_tag='<:orienta:1250903370894671963>\'s',
    description='Если тебе (внезапно) неприятно долго ожидать в очереди, чтобы зайти на сервер, ты можешь купить '
                'этот товар и заходить на него быстрее других игроков.',
    image_url='https://media.discordapp.net/attachments/1162830763390140548/1250350926716473465/Queue.png'
              '?ex=666a9f8b&is=66694e0b&hm=1bff6892241431d60d80ec58f24fe78b7bc8407dd5ec3d0740271f940c45ef1f&='
              '&format=webp&quality=lossless&width=725&height=671',
    emoji='⏩',
    func=functions.priority_queue
)


async def get_products():
    return colored_nick, gigachat_access, ban_annulment, priority_queue