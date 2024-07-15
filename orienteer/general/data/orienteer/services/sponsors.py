from uuid import UUID
from datetime import timedelta, datetime


async def set_sponsor(user_id: UUID, tier: int, duration: timedelta = timedelta(days=31),
                      ooc_color='ffffff') -> str:
    result = ''

    # TODO: FIX THIS
    if 'tier < 0 or tier > 4' is not None:
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

        sponsor_data.add_info(user_id, tier, ooc_color,
                              allowed_markings, ghost_theme, expires_in)

    result += '- файл записал, все оке))'
    return result


async def get_sponsor_level(user_id: UUID) -> tuple[str | None, int | None]:
    return 'PLACEHOLDER', 0xfd123d

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

    level += f'\nИстекает: {SponsorData().get_expires_in(
        user_id).strftime("%d.%m.%Yг. %H:%M")}'
    return level, color
