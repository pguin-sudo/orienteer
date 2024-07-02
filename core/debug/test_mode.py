from core.config import Debug

debug_message = ''
debug_url = ''

if Debug.MODE:
    debug_message = 'Бот запущен в тестовом режиме при обнаружении любого бага писать @mocviu'
    debug_url = ('https://cdn.discordapp.com/attachments/1247233955590180896/1249057919601868952/'
                 '128px-GNOME_Terminal_icon_2019.svg.png?ex=6665eb56&is=666499d6&'
                 'hm=fc9958dcae1190b0b2de840512df4c7d52eaf25b78aba3bc1d3b8ea0483ec9dd&')
