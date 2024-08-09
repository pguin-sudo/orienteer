import disnake

from orienteer.general.config import DEBUG_MODE

DEBUG_FOOTER_CONTENT = 'Бот запущен в тестовом режиме, при обнаружении любого бага писать @mocviu'
DEBUG_FOOTER_IMAGE = ('https://media.discordapp.net/attachments/847146486969008129/1271010621747630131/debug-icon'
                      '-design-free-vector.jpg?ex=66b5c862&is=66b476e2&hm'
                      '=362919a91e6430722a8eb044bd2ba72dd8276d810518ce301b8b28801dfad8d9&=&format=webp&width=701'
                      '&height=701')


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


def success_message(title='Успех', content='', color=0x3cdb30, footer=''):
    color = 0x3cdb30 if color is None else color
    return _base_embed(title='✅ ' + title, content=content, color=color, footer=footer)


def result_message(title='Результат:', content='', color=0x5c85d6):
    color = 0x5c85d6 if color is None else color
    return _base_embed(title=title, content=content, color=color)


def char_embed(title='Неизвестный персонаж', content='', color=0xfff):
    color = 0xfff if color is None else color
    return _base_embed(title=title, content=content, color=color)
