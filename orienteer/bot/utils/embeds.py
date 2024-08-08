import disnake

from orienteer.general.config import DEBUG_MODE

DEBUG_FOOTER_CONTENT = 'Бот запущен в тестовом режиме, при обнаружении любого бага писать @mocviu'
DEBUG_FOOTER_IMAGE = ('https://cdn.discordapp.com/attachments/1247233955590180896/1249057919601868952/'
                      '128px-GNOME_Terminal_icon_2019.svg.png?ex=6665eb56&is=666499d6&'
                      'hm=fc9958dcae1190b0b2de840512df4c7d52eaf25b78aba3bc1d3b8ea0483ec9dd&')


def _base_embed(title='', content='', color=0x38383d, footer=''):
    embed = disnake.Embed(title=title, description=content, color=color)

    if footer:
        embed.set_footer(text=footer)
    elif DEBUG_MODE:
        embed.set_footer(text=DEBUG_FOOTER_CONTENT, icon_url=DEBUG_FOOTER_IMAGE)

    return embed


def error_message(title='Ошибка', content='', color=0xdb3c30, footer=''):
    color = 0xdb3c30 if color is None else color
    return _base_embed(title='<:beer:1180521543390986324> ' + title, content=content, color=color, footer=footer)


def success_message(title='Успех', content='', color=0x3cdb30):
    color = 0x3cdb30 if color is None else color
    return _base_embed(title='✅ ' + title, content=content, color=color)


def result_message(title='Результат:', content='', color=0x5c85d6):
    color = 0x5c85d6 if color is None else color
    return _base_embed(title=title, content=content, color=color)


def char_embed(title='Неизвестный персонаж', content='', color=0xfff):
    color = 0xfff if color is None else color
    return _base_embed(title=title, content=content, color=color)
