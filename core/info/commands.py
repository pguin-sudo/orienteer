import json
from typing import Any
from uuid import UUID

import requests
import discord
from discord import Colour
from datetime import date, datetime, timedelta, timezone

from core.data import ss14, discord_time, orientiks, formulas
from core.data.discord_time import timedelta_to_russian_text
from core.data.sponsor_data import SponsorData

roles_description = 'Показывает всё время, наигранное на сервере'
bans_description = 'Показывает все, полученные на сервере, баны игрока, а также общий штраф за них'
profile_description = 'Показывает профиль игрока, а именно, общее время и репутацию'
reputation_description = ('Показывает репутацию и значение "респектабельности" игрока, а также штрафы за полученные '
                          'блокировки')
char_description = 'Выводит общую информацию о персонажах игрока'
status_description = 'Показывает статус сервера'

balance_description = 'Выводит количество Ориентиков'
transfer_description = 'Переводит часть <:orienta:1250903370894671963>\'s другому человеку'
shop_description = 'Открывает магазин'

promo_description = 'Выполняет промокод'

change_color_description = 'Изменяет цвет спонсора, который ввел команду'


async def set_sponsor(user_id: UUID, tier: int, duration: timedelta = timedelta(days=31),
                      ooc_color='ffffff') -> str:
    result = ''

    if tier < 0 or tier > 4:
        result += 'ERROR#1. Неверное значение уровня подписки'
        return result

    sponsor_data = SponsorData()

    if sponsor_data.get_info(user_id) is not None:
        if tier == 0:
            result += '- очистка\n'

            sponsor_data.delete_info(user_id)

            await ss14.delete_from_whitelist(user_id)
            result += f'- "whitelist удален"\n'

        else:
            result += 'ERROR#3. Существующие записи можно только удалить. Для этого указывай уровень подписки 0'
            return result
    else:
        result += '- добавление\n'
        allowed_markings = ['marking1', 'marking2']
        ghost_theme = "dark"

        if tier == 0:
            result += 'ERROR#4. Нельзя добавить запись с уровнем подписки 0'
            return result
        elif tier > 1:
            allowed_markings = ('CatEars', 'CatTail', 'HumanFacialHairHandlebar', 'HumanHairWife', 'HumanHairSpicy',
                                'HumanHairShy', 'HumanHairQuadcurls', 'HumanHairLooseSlicked',
                                'HumanHairLongdtails',
                                'HumanHairFortunetellerAlt', 'HumanHairFortuneteller', 'HumanHairFingerwave',
                                'CatEarsTorn', 'CatTailStripes', 'HumanHairCotton', 'CatEarsCurled',
                                'CatEarsStubby',
                                'SlimeCatEars', 'SlimeCatTail', 'SlimeCatEarsStubby', 'SlimeCatEarsCurled',
                                'SlimeCatEarsTorn', 'SlimeCatTailStripes')

            ghost_theme = "flameTheme"

            if await ss14.check_whitelist(user_id):
                result += f'- вайтлист уже был выдан давно\n'
            else:
                await ss14.add_to_whitelist(user_id)
                result += f'- whitelist выдан\n'

            if tier > 2:
                ans = await add_all_time(user_id, 1)
                result += f'- {ans}\n'

            if tier == 4:
                result += '- а теперь выдай маркинги\n'

        expires_in = datetime.now() + duration

        sponsor_data.add_info(user_id, tier, ooc_color, allowed_markings, ghost_theme, expires_in)

    result += '- файл записал, все оке))'
    return result


async def get_status() -> tuple[str, str, int]:
    try:
        result = requests.get(f'https://central.spacestation14.io/hub/api/servers/')
    except Exception as e:
        return 'Статус "Amadis ⚔️" - <:beer:1180521543390986324>:', '**Нет данных**', 0xeb0c17

    servers = json.loads(result.text)

    for server in servers:
        if server['address'] != 'ss14://amadis.orientacorp.ru:1313':
            continue

        status = server['statusData']

        preset = status["preset"]
        hidden_preset = preset if not preset in ('Ядерные оперативники', 'Предатели') else 'Секрет'

        text = (f'**Режим:** {hidden_preset}\n'
                f'**Игроки:** {status["players"]}/{status["soft_max_players"]}\n'
                f'**Раунд №**{status["round_id"]}')

        run_level = status['run_level']
        if run_level == 0:
            text += '\n**Загрузка раунда**'
            color = 0xbb61e8
        elif run_level == 1:
            time_string = status['round_start_time']

            given_time = datetime.strptime(time_string[:-9], '%Y-%m-%dT%H:%M:%S')
            current_time = datetime.now() + timedelta(hours=-3)

            # print(time_string, given_time, current_time)
            time_difference = current_time - given_time

            text += f'\n**Продолжительность раунда:** {await timedelta_to_russian_text(time_difference)}'
            text += f'\n**Карта:** {status["map"]}'
            color = 0x5c85d6
        else:
            color = 0xeb0c17

        if status['panic_bunker']:
            text += '\n**Бункер**'
            color = 0xeb0c17

        return 'Статус "Amadis ⚔️" - <:nobeer:1180521621212114995>:', text, color

    return 'Статус "Amadis ⚔️" -  <:beer:1180521543390986324>:', '**Сервер выключен**', 0xeb0c17


async def get_admin_rank(user_id: UUID):
    admin_rank_id = await ss14.get_admin_rank_id(user_id)

    if admin_rank_id is None:
        return False

    name = await ss14.get_rank_name(admin_rank_id)
    if name is None:
        return False

    return name


async def get_sponsor_level(user_id: UUID) -> tuple[str | None, Colour | None]:
    tier = SponsorData().get_tier(user_id)
    if not tier:
        return None, None

    tier = int(tier)

    if tier == 0:
        return None, None

    if tier == 1:
        level = 'Космический курсант'
    elif tier == 2:
        level = 'Капитан'
    elif tier == 3:
        level = 'Адмирал Orienta'
    elif tier == 4:
        level = 'Директор корпорации Orienta'
    else:
        level = 'Нет данных'

    ooc_color = SponsorData().get_color(user_id)
    color = discord.Colour.from_rgb(int(ooc_color.lstrip('#')[0:0 + 2], 16),
                                    int(ooc_color.lstrip('#')[2:2 + 2], 16),
                                    int(ooc_color.lstrip('#')[4:4 + 2], 16))

    level += f'\nИстекает: {SponsorData().get_expires_in(user_id).strftime("%d.%m.%Yг. %H:%M")}'
    return level, color


async def add_playtime(user_id: UUID, tracker: str, minutes: int) -> str:
    await ss14.add_playtime(user_id, tracker, minutes)

    if tracker == 'Overall':
        return f'Общее: {await timedelta_to_russian_text(timedelta(minutes))}\n\n'
    else:
        return f'{get_job_description(tracker)[1]}: {await timedelta_to_russian_text(timedelta(minutes))}\n'


async def add_all_time(user_id: UUID, percent) -> str:
    full_time = {
        "Overall": 2500,
        "JobMedicalOfficer": 900,
        "JobScientist": 900,
        "JobStationEngineer": 900,
        "JobCargoTechnician": 900,
        "JobHeadOfPersonnel": 400,
        "JobSecurityOfficer": 900,
        "JobAtmosphericTechnician": 1000,
        "JobWarden": 600,
        "JobCaptain": 1700,
        "JobMedicalDoctor": 300,
        "JobMedicalIntern": 300,
        "JobSalvageSpecialist": 600,
        "JobChemist": 600
    }
    result = ''
    for tracker in full_time.keys():
        await ss14.add_playtime(user_id, tracker, int(full_time[tracker] * percent))
        result += f'{tracker}: {int(full_time[tracker] * percent)}\n'
    return result


async def update_user_roles(user_id: UUID, jobs: dict) -> str:
    roles_text = ''
    for tracker, minutes in jobs.items():
        await add_playtime(user_id, tracker, minutes)
        if tracker == 'Overall':
            roles_text += f'Общее: {await timedelta_to_russian_text(timedelta(minutes))}\n\n'
        else:
            roles_text += f"{get_job_description(tracker)[1]}: {await timedelta_to_russian_text(timedelta(minutes))}\n"
    return roles_text


async def try_promo(discord_user_id: int, user_id: UUID, code: str) -> tuple[bool, str, str]:
    code = code.lower()

    data = await ss14.get_promo_data(code)
    if not data:
        return False, 'Отказ!', 'Такого промокода не существует!'

    if data['usages'] <= 0:
        return False, 'Отказ!', 'Промокод уже был использован максимальное количество раз!'

    for tracker, time_needed in json.loads(data['dependencies']).items():
        time = await ss14.get_playtime_timedelta(user_id, tracker)
        if not time:
            return False, 'Отказ!', 'Нет информации о наигранном времени!'
        elif time.total_seconds() / 60 < time_needed:
            return False, 'Отказ!', 'Недостаточно наигранного времени для выполения промокода!'

    if data['for'] < date.today():
        return False, 'Отказ!', 'Срок промокода истек!'

    if await ss14.check_promo_already_used_discord(discord_user_id, code):
        return False, 'Отказ!', 'Промокод уже был использован от имени этого пользователя!'

    if await ss14.check_promo_already_used_ss14(user_id, code):
        return False, 'Отказ!', 'Промокод уже был использован для этого ckey!'

    creator_code = await ss14.get_creator_code(user_id)

    is_creators_code = data['creator']
    if is_creators_code and creator_code is not None:
        return False, 'Отказ!', f'Промокод креатора уже был использован! ({creator_code})'

    roles_text = ''

    for tracker, minutes in json.loads(data['jobs']).items():
        roles_text = await add_playtime(user_id, tracker, minutes) + '\n'

    await ss14.mark_promo_as_used(user_id, discord_user_id, code)

    await ss14.decrease_promo_usages(code)

    return (True, 'Промокод успешно использован!',
            (
                f'Вы получили: {roles_text}\n' + f'Теперь вы поддерживаете креатора \"{code}\"' if is_creators_code else ''))


async def get_profit(code) -> str | None:
    users = await ss14.get_users_by_promo_code(code)
    if users:
        cringe_usages = await ss14.get_cringe_usages_by_promo_code(code)
        return (f'С последней выплаты: {10000 - cringe_usages} исп.\n'
                f'На счете: {(10000 - cringe_usages) * 3} руб.\n'
                f'\n'
                f'Всего: {users} исп.\n'
                f'Общая прибыль: {users * 3} руб.')
    return None


async def closest_color(hex_code):
    color_names = {
        '#000000': 'Черный',
        '#808080': 'Серый',
        '#c0c0c0': 'Серебряный',
        '#ffffff': 'Белый',
        '#ff00ff': 'Маджента',
        '#800080': 'Пурпурный',
        '#ff0000': 'Красный',
        '#800000': 'Коричнево-малиновый',
        '#ffff00': 'Жёлтый',
        '#808000': 'Оливковый',
        '#00ff00': 'Лайм',
        '#008000': 'Зелёный',
        '#008080': 'Окраски птицы чирок',
        '#0000ff': 'Синий',
        '#000080': 'Форма морских офицеров',
        '#f5f5f5': 'Дымчато-белый',
        '#dcdcdc': 'Гейнсборо',
        '#d3d3d3': 'Светло серый',
        '#a9a9a9': 'Темно серый',
        '#696969': 'Тусклый серый',
        '#778899': 'Светлый аспидно-серый',
        '#708090': 'Серый шифер',
        '#2f4f4f': 'Аспидно-серый',
        '#f08080': 'Светло-коралловый',
        '#fa8072': 'Лососевый',
        '#E9967A': 'Тёмно-лососёвый',
        '#ffa07a': 'Светло-лососёвый',
        '#dc143c': 'Малиновый',
        '#cd5c5c': 'Индийский красный',
        '#b22222': 'Кирпичный',
        '#a52a2a': 'Коричнево-бордовый',
        '#8b0000': 'Тёмно-красный',
        '#fff5ee': 'Цвет морской раковины',
        '#f5f5dc': 'Бежевый',
        '#fdf5e6': 'Старое кружево',
        '#fffaf0': 'Цветочный белый',
        '#faebd7': 'Белый антик',
        '#faf0e6': 'Льняной',
        '#ffebcd': 'Очищенный миндаль',
        '#ffe4c4': 'Бисквитный',
        '#ffdead': 'Белый навахо',
        '#f5deb3': 'Пшеничный',
        '#deb887': 'Плотная древесина',
        '#d2b48c': 'Цвет загара',
        '#f4a460': 'Красный песок',
        '#daa520': 'Золотисто-березовый',
        '#b8860b': 'Тёмный золотарник',
        '#d2691e': 'Шоколадный',
        '#8b4513': 'Кожаного седла для лошади',
        '#a0522d': 'Сиена',
        '#ff7f50': 'Коралловый',
        '#ff6347': 'Томатный',
        '#ff4500': 'Оранжево-красный',
        '#ff8c00': 'Тёмно-оранжевый',
        '#ffa500': 'Оранжевый',
        '#fff8dc': 'Цвет пестиков неспелой кукурузы',
        '#fffff0': 'Слоновая кость',
        '#ffffe0': 'Светло-жёлтый',
        '#fffacd': 'Лимонно-кремовый',
        '#fafad2': 'Светло-жёлтый золотистый',
        '#ffefd5': 'Побег папайи',
        '#ffe4b5': 'Мокасиновый',
        '#ffdab9': 'Тёмно-персиковый',
        '#eee8aa': 'Бледно-золотистый',
        '#f0e68c': 'Светлый хаки',
        '#bdb76b': 'Тёмный хаки',
        '#ffd700': 'Золотой',
        '#f0fff0': 'Медовая роса',
        '#f5fffa': 'Мятно-кремовый',
        '#adff2f': 'Зелёно-жёлтый',
        '#7fff00': 'Шартрёз',
        '#7cfc00': 'Зелёная лужайка',
        '#32cd32': 'Лаймово-зелёный',
        '#98fb98': 'Бледный зелёный',
        '#90ee90': 'Светло-зелёный',
        '#00fa9a': 'Умеренный весенний зелёный',
        '#00ff7f': 'Весенне-зелёный',
        '#3cb371': 'Умеренно-зелёное море',
        '#2e8b57': 'Зелёное море',
        '#228b22': 'Лесной зелёный',
        '#006400': 'Очень тёмный лимонный зеленый',
        '#9acd32': 'Жёлто-зелёный',
        '#6b8e23': 'Нежно-оливковый',
        '#556b2f': 'Тёмный оливково-зеленый',
        '#66cdaa': 'Умеренный аквамариновый',
        '#8fbc8f': 'Тёмное зелёное море',
        '#20b2aa': 'Светлое зелёное море',
        '#008b8b': 'Тёмный циан',
        '#f0ffff': 'Небесная лазурь',
        '#f0f8ff': 'Синяя Элис',
        '#e0ffff': 'Светлый циан',
        '#00ffff': 'Циан,цвет морской волны',
        '#7fffd4': 'Аквамариновый',
        '#40e0d0': 'Светло-бирюзовый',
        '#48d1cc': 'Умеренно-бирюзовый',
        '#00ced1': 'Тёмно-бирюзовый',
        '#afeeee': 'Бледно-синий',
        '#b0e0e6': 'Пыльный голубой',
        '#add8e6': 'Светлый синий',
        '#b0c4de': 'Светлый стальной синий',
        '#87ceeb': 'Городское небо',
        '#87cefa': 'Светло-голубой',
        '#00bfff': 'Морозное небо',
        '#1e90ff': 'Защитно-синий',
        '#6495ed': 'Васильковый',
        '#7b68ee': 'Умеренный аспидно-синий',
        '#5f9ea0': 'Кадетский синий',
        '#4682b4': 'Синяя сталь',
        '#4169e1': 'Королевский синий',
        '#0000cd': 'Средний синий',
        '#00008b': 'Тёмный ультрамариновый',
        '#191970': 'Полуночный чёрный',
        '#6a5acd': 'Аспидно-синий',
        '#483d8b': 'Тёмный аспидно-синий',
        '#f8f8ff': 'Призрачно-белый',
        '#e6e6fa': 'Лаванда',
        '#d8bfd8': 'Чертополох',
        '#dda0dd': 'Светлая слива',
        '#ee82ee': 'Розово-фиолетовый',
        '#da70d6': 'Орхидея',
        '#c71585': 'Умеренный фиолетово-красный',
        '#ba55d3': 'Умеренный цвет орхидеи',
        '#9370db': 'Умеренный пурпурный',
        '#8a2be2': 'Сине-лиловый',
        '#9400d3': 'Тёмно-фиолетовый',
        '#9932cc': 'Тёмная орхидея',
        '#8b008b': 'Тёмный маджента',
        '#4b0082': 'Индиго',
        '#fffafa': 'Белоснежный',
        '#fff0f5': 'Розово-лавандовый',
        '#ffe4e1': 'Тускло-розовый',
        '#ffc0cb': 'Розовый',
        '#ffb6c1': 'Светло-розовый',
        '#ff69b4': 'Ярко-розовый',
        '#ff1493': 'Глубокий розовый',
        '#db7093': 'Лиловый',
        '#bc8f8f': 'Розово-коричневый'
    }

    r = int(hex_code[1:3], 16)
    g = int(hex_code[3:5], 16)
    b = int(hex_code[5:], 16)

    min_diff = float('inf')
    nearest_key = None

    for key in color_names:
        r_key = int(key[1:3], 16)
        g_key = int(key[3:5], 16)
        b_key = int(key[5:], 16)

        diff = ((r - r_key) ** 2 + (g - g_key) ** 2 + (b - b_key) ** 2) ** 0.5

        if diff < min_diff:
            min_diff = diff
            nearest_key = key

    return color_names[nearest_key]


def get_job_description(job):
    job_dict = {
        'JobCargoTechnician': (4, 'Грузчик'),
        'JobSalvageSpecialist': (4, 'Утилизатор'),

        'JobBartender': (0, 'Бармен'),
        'JobBotanist': (0, 'Ботаник'),
        'JobBoxer': (0, 'Боксёр'),
        'JobChaplain': (0, 'Священник'),
        'JobChef': (0, 'Шеф-повар'),
        'JobClown': (0, 'Клоун'),
        'JobJanitor': (0, 'Уборщик'),
        'JobLawyer': (0, 'Юрист'),
        'JobLibrarian': (0, 'Библиотекарь'),
        'JobMime': (0, 'Мим'),
        'JobMusician': (0, 'Музыкант'),
        'JobPassenger': (0, 'Пассажир'),
        'JobReporter': (0, 'Репортёр'),
        'JobZookeeper': (0, 'Зоотехник'),
        'JobServiceWorker': (0, 'Сервисный работник'),
        'JobVisitor': (0, 'Посетитель'),

        'JobCaptain': (7, 'Капитан'),
        'JobIAA': (7, 'Юрист'),
        'JobChiefEngineer': (7, 'Старший инженер'),
        'JobChiefMedicalOfficer': (7, 'Главный врач'),
        'JobMedicalOfficer': (7, 'Главный врач'),
        'JobHeadOfPersonnel': (7, 'Глава персонала'),
        'JobHeadOfSecurity': (7, 'Глава службы безопасности'),
        'JobResearchDirector': (7, 'Научный руководитель'),
        'JobQuartermaster': (7, 'Квартирмейстер'),
        'JobBlueShield': (7, 'Офицер "Синий щит"'),

        'JobAtmosphericTechnician': (1, 'Атмосферный техник'),
        'JobStationEngineer': (1, 'Инженер'),
        'JobTechnicalAssistant': (1, 'Технический ассистент'),

        'JobChemist': (2, 'Химик'),
        'JobMedicalDoctor': (2, 'Врач'),
        'JobMedicalIntern': (2, 'Интерн'),
        'JobPsychologist': (2, 'Психолог'),
        'JobParamedic': (2, 'Парамедик'),
        'JobPathologist': (2, 'Патологоанатом'),
        'JobSeniorPhysician': (2, 'Ведущий врач'),

        'JobSecurityCadet': (3, 'Кадет СБ'),
        'JobSecurityOfficer': (3, 'Офицер СБ'),
        'JobDetective': (3, 'Детектив'),
        'JobWarden': (3, 'Смотритель'),
        'JobBrigmedic': (3, 'Бригмедик'),
        'JobPrisoner': (3, 'Заключенный'),
        'JobSeniorOfficer': (3, 'Инструктор СБ'),
        'JobOverseer': (3, 'Надзиратель'),

        'JobScientist': (5, 'Учёный'),
        'JobResearchAssistant': (5, 'Научный ассистент'),
        'JobSeniorResearcher': (5, 'Ведущий учёный'),

        'JobBorgSecurity': (6, 'Борг СБ'),
        'JobBorgMedical': (6, 'Медицинский борг'),
        'JobBorgEngineer': (6, 'Инженерный борг'),
        'JobBorgJunitor': (6, 'Уборочный борг'),
        'JobBorgMining': (6, 'Шахтёрский борг'),
        'JobBorg': (6, 'Борг'),

        'BPLAMED': (6, 'Медицинский дрон'),
        'BPLATech': (6, 'Технический дрон'),

        'JobCentralCommandOfficial': (8, 'Представитель ЦК'),
        'JobCentralCommandAssistant': (8, 'Ассистент ОЦК'),
        'JobCentralCommandCargo': (8, 'Грузчик ЦК'),
        'JobCentralCommandSecOfficer': (8, 'Приватный офицер ЦК'),
        'JobCentralCommandOperator': (8, 'Оператор ЦК'),
        'JobCentralCommandSecGavna': (8, 'Начальник безопасности ЦК'),

        'JobExplorer': (9, 'Исследователь'),
        'JobStudent': (9, 'Ученик'),
        'JobFreelancerGear': (9, 'Фрилансер'),
        'JobFugitive': (9, 'Беглец'),
        'JobERTEngineer': (9, 'Инженер ОБР'),
        'JobERTJanitor': (9, 'Уборщик ОБР'),
        'JobERTLeader': (9, 'Лидер ОБР'),
        'JobERTMedical': (9, 'Медик ОБР'),
        'JobERTSecurity': (9, 'Офицер безопасности ОБР')
    }
    return job_dict.get(job, (9, job))


async def get_all_char(user_id: UUID):
    preference = await ss14.get_user_preference(user_id)
    profiles = await ss14.get_user_profiles(preference)

    embeds = list()
    for profile in profiles:
        if profile[2] is not None and profile[2] != 'поменяйте ник пожалуйста':
            field_title = f'**{profile[2]}**'
        else:
            field_title = '**Без имени**'
        if profile[16] == 'Moth':
            field_description = f'**Моль**,'
        elif profile[16] == 'Human':
            field_description = f'**Человек**,'
        elif profile[16] == 'Unath':
            field_description = f'**Унатх,**'
        elif profile[16] == 'Vox':
            field_description = f'**Вокс,**'
        elif profile[16] == 'Dwarf':
            field_description = f'**Дварф,**'
        elif profile[16] == 'Felinid':
            field_description = f'**Фелинид,**'
        elif profile[16] == 'Reptilian':
            field_description = f'**Унатх,**'
        elif profile[16] == 'SlimePerson':
            field_description = f'**Слаймолюд,**'
        elif profile[16] == 'HumanoidFoxes':
            field_description = f'**Вульпканин,**'
        elif profile[16] == 'Oni':
            field_description = f'**Óни,**'
        else:
            field_description = f'{profile[16]},'

        field_description += f' {profile[3]} лет\n'

        if profile[4] == 'Male':
            field_description += '**Мужчина**\n'
        elif profile[4] == 'Female':
            field_description += '**Женщина**\n'
        else:
            field_description += '**Небинарная личность**\n'

        if profile[5] == 'HairBald':
            field_description += f'**Лысый**\n'
        else:
            field_description += f'**Цвет волос:** {await closest_color(profile[6])}\n'

        if profile[7] != 'FacialHairShaved':
            field_description += f'**Цвет растительности:** {await closest_color(profile[8])}\n'
        field_description += f'**Цвет глаз:** {await closest_color(profile[9])}\n'

        embeds.append(discord.Embed(color=discord.Colour.from_rgb(int(profile[10].lstrip('#')[0:0 + 2], 16),
                                                                  int(profile[10].lstrip('#')[2:2 + 2], 16),
                                                                  int(profile[10].lstrip('#')[4:4 + 2], 16)),
                                    title=field_title, description=field_description))
        return embeds


async def get_last_seen_time(user_id: UUID):
    result = await ss14.get_last_seen_time(user_id)

    if result is None:
        return 'Нет информации'

    time = await discord_time.get_discord_datetime_tag(result)
    return time


async def get_first_seen_time(user_id: UUID):
    result = await ss14.get_last_seen_time(user_id)

    if result is None:
        return 'Нет информации'

    time = await discord_time.get_discord_datetime_tag(result)
    return time


async def get_ban_status(user_id: UUID) -> int:
    """
    0 - Без банов
    1 - Временный
    2 - Пермач
    """
    ban = await ss14.get_last_ban(user_id)

    if ban is None:
        return 0
    elif ban:
        if ban['expiration_time'] is None:
            return 2
        if ban['expiration_time'] > datetime.now(timezone.utc):
            return 1
    else:
        return 0


async def get_all_bans(user_id: UUID) -> discord.Embed:
    embed = discord.Embed(color=0xee0000, title=f'Баны {await ss14.get_ckey(user_id)}:')

    bans = await ss14.get_bans(user_id)
    total_fine = 0

    for ban in bans:
        (server_ban_id, player_user_id, address, ban_time, expiration_time,
         reason, banning_admin, hwid, exempt_flags, auto_delete,
         hidden, last_edited_at, last_edited_by_id, playtime_at_note, round_id,
         severity) = ban

        admin_name = await ss14.get_ckey(banning_admin) if banning_admin is not None else 'Неизвестно'
        ban_time_str = await discord_time.get_discord_datetime_tag(ban_time)

        if expiration_time is None:
            expiration_time_str = 'Никогда'
            fine = '∞'
        else:
            expiration_time_str = await discord_time.get_discord_datetime_tag(expiration_time)
            fine = await formulas.calculate_fine(expiration_time - ban_time)
            total_fine += fine

        field_title = f'**Бан** {server_ban_id}'
        field_description = f'**Администратор:** {admin_name}\n'
        field_description += f'**Время получения:** {ban_time_str}\n'
        field_description += f'**Время снятия:** {expiration_time_str}\n'
        field_description += f'**Штраф:** {fine} <:orienta:1250903370894671963>\'s\n'
        field_description += f'**Причина:** {reason.capitalize()}\n'

        embed.add_field(name=field_title, value=field_description, inline=False)

    if total_fine > 0:
        embed.description = f'Итого со штрафов: -{total_fine} <:orienta:1250903370894671963>\'s'
    return embed


async def get_rep(user_id: UUID) -> str:
    ban_records = await ss14.get_bans(user_id)

    result = await ss14.fetch_reputation_value(user_id)

    if result is None or not result:
        reputation_value = 1000
        # respect_value = 0
    else:
        reputation_value = result
        # respect_value = result

    fine = 0

    for ban in ban_records:
        (server_ban_id, player_user_id, address, ban_time, expiration_time,
         reason, banning_admin, hwid, exempt_flags, auto_delete,
         hidden, last_edited_at, last_edited_by_id, playtime_at_note, round_id,
         severity) = ban

        if expiration_time is not None:
            fine += await formulas.calculate_fine(expiration_time - ban_time)

    reputation_value -= fine
    res = f'Штрафы за баны: {fine} <:orienta:1250903370894671963>\'s'
    return res


async def get_all_roles(user_id: UUID) -> list[str | Any] | None:
    results = await ss14.get_all_playtime(user_id)

    desc = ['', '', '', '', '', '', '', '', '', '', '']

    if len(results) > 0:
        desc[10] = '**Общее время**: '
        for row in results:
            if row[2] == 'Overall':
                desc[10] = f'{await timedelta_to_russian_text(row[3])}\n\n'
            else:
                desc[int(get_job_description(row[2])[0])] += (
                    f'- **{get_job_description(row[2])[1]}**: '
                    f'{await timedelta_to_russian_text(row[3])}\n')
        return desc
    else:
        return None


async def get_most_popular_role(user_id: UUID):
    results = await ss14.get_all_playtime(user_id)

    if results:
        favorite_role = None
        max_play_time = timedelta()

        for row in results:
            if row[2] in ('Overall',):
                continue

            if row[3] > max_play_time:
                max_play_time = row[3]
                favorite_role = row[2]

        if favorite_role:
            return f'{get_job_description(favorite_role)[1]} - {await timedelta_to_russian_text(max_play_time)}'
        else:
            return None
    else:
        return None


async def change_ooc_color(user_id: UUID, color: str) -> str:
    SponsorData().set_color(user_id, color)
    return 'Цвет успешно изменен'


# orientiks
async def get_balance(user_id: UUID) -> str:
    return str(await orientiks.get_balance(user_id)) + ' <:orienta:1250903370894671963>\'s'


async def do_transfer(sender_user_id: UUID, recipient_user_id: UUID, amount: int) -> None:
    await ss14.set_orientiks_from_friends(sender_user_id, -amount)
    await ss14.set_orientiks_from_friends(recipient_user_id, amount)
