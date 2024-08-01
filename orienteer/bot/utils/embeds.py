import disnake

from orienteer.general.config import DEBUG_MODE

_debug_message_content = 'Бот запущен в тестовом режиме при обнаружении любого бага писать @mocviu'
_debug_message_img_url = ('https://cdn.discordapp.com/attachments/1247233955590180896/1249057919601868952/'
                          '128px-GNOME_Terminal_icon_2019.svg.png?ex=6665eb56&is=666499d6&'
                          'hm=fc9958dcae1190b0b2de840512df4c7d52eaf25b78aba3bc1d3b8ea0483ec9dd&')


def _base_embed(title='', content='', color=0x38383d):
    embed = disnake.Embed(title=title, description=content, color=color)
    if DEBUG_MODE:
        embed.set_footer(text=_debug_message_content, icon_url=_debug_message_img_url)
    return embed


def error_message(title='Ошибка', content=''):
    return _base_embed(title='<:beer:1180521543390986324> ' + title, content=content, color=0xdb3c30)


def success_message(title='Успех', content=''):
    return _base_embed(title='✅ ' + title, content=content, color=0x3cdb30)


def result_message(title='Результат:', content='', color=0x5c85d6):
    return _base_embed(title=title, content=content, color=color)


def char_embed(title='Неизвестный персонаж', content='', color=0xfff):
    return _base_embed(title=title, content=content, color=color)
