import asyncio
import os

from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

from data.ss14 import get_user_id, get_user_id_by_discord_user_id, get_creator_code, get_discord_user_id_by_user_id

from core.info.commands import *

from core.config.main import Bot, Private, Roles

from core.debug.test_mode import debug_message, debug_url
from core.shop.slots import get_products

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=Bot.PREFIX, intents=intents)

bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(
        '⚛ Corporation Orienta | ⚔️ Amadis'))
    await bot.wait_until_ready()
    print(bot.guilds)
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@bot.tree.command(name='help', description='Выводит спиок всех доступных команд.', nsfw=False)
async def help(interaction: discord.Interaction):
    await interaction.response.defer()

    embed = discord.Embed(color=0x5c85d6, title='Список команд:')

    embed.add_field(name='status', value=status_description, inline=False)
    embed.add_field(name='roles <ckey>', value=roles_description, inline=False)
    embed.add_field(name='bans <ckey>', value=bans_description, inline=False)
    embed.add_field(name='profile <ckey>', value=profile_description, inline=False)
    embed.add_field(name='char <ckey>', value=char_description, inline=False)
    embed.add_field(name='promo <ckey> <code>', value=promo_description, inline=False)

    embed.add_field(name='balance <ckey>', value=balance_description, inline=False)

    embed.add_field(name='Скоро: change_color <color>', value=change_color_description, inline=False)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name='roles', description=roles_description, nsfw=False)
@app_commands.describe(ckey='C-key')
async def roles(interaction: discord.Interaction, ckey: str | None):
    await interaction.response.defer()

    if ckey is not None:
        ckey = ckey.replace(' ', '')

        user_id = await get_user_id(ckey)

        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
    else:
        user_id = await get_user_id_by_discord_user_id(interaction.user.id)
        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!',
                                  description='Ваш аккаунт Discord не привязан к SS14.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
        ckey = await ss14.get_ckey(user_id)

    all_roles = await get_all_roles(user_id)
    if all_roles is None:
        roles_embed = discord.Embed(color=0xee0000, title=f'Игрок {ckey} не молодец!',
                                    description=f'У него времени 0 секунд')
    else:
        roles_embed = discord.Embed(color=0x5c85d6, title=f'Наигранное время у {ckey}:',
                                    description=f'{all_roles[10]}')

        '' if all_roles[0] == '' else roles_embed.add_field(name='Сервисный отдел:', value=all_roles[0],
                                                            inline=False)
        '' if all_roles[1] == '' else roles_embed.add_field(name='Инженерный отдел:', value=all_roles[1],
                                                            inline=False)
        '' if all_roles[2] == '' else roles_embed.add_field(name='Медицинский отдел:', value=all_roles[2],
                                                            inline=False)
        '' if all_roles[3] == '' else roles_embed.add_field(name='Служба безопасности:', value=all_roles[3],
                                                            inline=False)
        '' if all_roles[4] == '' else roles_embed.add_field(name='Отдел снабжения:', value=all_roles[4],
                                                            inline=False)
        '' if all_roles[5] == '' else roles_embed.add_field(name='Научный отдел:', value=all_roles[5], inline=False)
        '' if all_roles[6] == '' else roles_embed.add_field(name='Синтеты:', value=all_roles[6], inline=False)
        '' if all_roles[7] == '' else roles_embed.add_field(name='Отдел командования:', value=all_roles[7],
                                                            inline=False)
        '' if all_roles[8] == '' else roles_embed.add_field(name='ЦентКом:', value=all_roles[8], inline=False)
        '' if all_roles[9] == '' else roles_embed.add_field(name='Другое:', value=all_roles[9], inline=False)

    await interaction.followup.send(embed=roles_embed)


@bot.tree.command(name='bans', description=bans_description, nsfw=False)
@app_commands.describe(ckey='C-key')
async def bans(interaction: discord.Interaction, ckey: str | None):
    await interaction.response.defer()

    if ckey is not None:
        ckey = ckey.replace(' ', '')

        user_id = await get_user_id(ckey)

        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
    else:
        user_id = await get_user_id_by_discord_user_id(interaction.user.id)
        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!',
                                  description='Ваш аккаунт Discord не привязан к SS14.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
        ckey = await ss14.get_ckey(user_id)

    embed = await get_all_bans(user_id)
    if embed.fields:
        embed.title = f'Сводка банов для {ckey}:'
    else:
        embed.title = f'Пользователь {ckey} не имеет банов.'
        embed.description = 'Молодец!'

    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name='profile', description=profile_description, nsfw=False)
@app_commands.describe(ckey='C-key')
async def profile(interaction: discord.Interaction, ckey: str | None):
    await interaction.response.defer()

    if ckey is not None:
        ckey = ckey.replace(' ', '')

        user_id = await get_user_id(ckey)

        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
    else:
        user_id = await get_user_id_by_discord_user_id(interaction.user.id)
        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!',
                                  description='Ваш аккаунт Discord не привязан к SS14.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
        ckey = await ss14.get_ckey(user_id)

    creator = await get_creator_code(user_id)
    first_seen = await get_first_seen_time(user_id)
    last_seen = await get_last_seen_time(user_id)
    all_roles = await get_all_roles(user_id)
    most_popular_role = await get_most_popular_role(user_id)
    sponsor_level, color = await get_sponsor_level(user_id)
    admin_rank = await get_admin_rank(user_id)
    is_in_whitelist = await ss14.check_whitelist(user_id)
    balance_info = await get_balance(user_id)
    ban_status = await get_ban_status(user_id)

    embed = discord.Embed(color=0x5c85d6, title=f'Профиль {ckey}:',
                          description=f'Первое появление: {first_seen}\n'
                                      f'Последнее появление: {last_seen}')

    if color is None:
        if ban_status == 0:
            embed.colour = 0x5c85d6
            ban_status = "Без блокировки"
        elif ban_status == 1:
            embed.colour = 0xe84f4f
            ban_status = "Временно заблокирован"
        elif ban_status == 2:
            embed.colour = 0x222222
            ban_status = "Бессрочно заблокирован"
    else:
        if ban_status == 0:
            ban_status = "Без блокировки"
        elif ban_status == 1:
            ban_status = "Временно заблокирован"
        elif ban_status == 2:
            ban_status = "Бессрочно заблокирован"
        embed.colour = color

    embed.add_field(name='Статус:', value=f'{ban_status}', inline=False)

    if creator is not None:
        embed.add_field(name='Код пригласителя:', value=f'{creator}', inline=False)

    if all_roles is not None:
        embed.add_field(name='Наигранное время:', value=f'Общее: {all_roles[10]}', inline=False)

    if most_popular_role is not None:
        embed.add_field(name='Любимя роль:', value=f'{most_popular_role}', inline=False)

    if sponsor_level is not None:
        embed.add_field(name='Уровень подписки:', value=sponsor_level, inline=False)

    if admin_rank:
        embed.add_field(name='Ранг администратора:', value=admin_rank, inline=False)

    if is_in_whitelist:
        embed.add_field(name='Whitelist:', value='Есть!', inline=False)
    else:
        embed.add_field(name='Whitelist:', value='Нет <:EDGEHOG:1106583346835898399>', inline=False)

    if balance_info is not None:
        embed.add_field(name='Баланс:', value=balance_info, inline=False)

    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed)


'''
@bot.tree.command(NAME='reputation', description=reputation_description, nsfw=False)
@app_commands.describe(ckey='C-key')
async def reputation(interaction: checker.Interaction, ckey: str):
    ckey = ckey.replace(' ', '')
    if ckey is None:
        await interaction.followup.send('Использование: "/reputation <ckey>"') 
        return
        
    user_id = await get_user_id(ckey)

    if user_id is None:
        embed = checker.Embed(color=0xee0000, title=f'Такого пользователя ({ckey}) нет!',
                                         description='Использование: "/reputation <ckey>"')
    else:
        rep_info = get_rep(user_id)
        embed = checker.Embed(color=0x5c85d6, title=f'Репутация {ckey}:', description=rep_info)

    await interaction.followup.send(embed=embed) 
    '''


@bot.tree.command(name='char', description=char_description, nsfw=False)
@app_commands.describe(ckey='C-key')
async def char(interaction: discord.Interaction, ckey: str | None):
    await interaction.response.defer()

    if ckey is not None:
        ckey = ckey.replace(' ', '')

        user_id = await get_user_id(ckey)

        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
    else:
        user_id = await get_user_id_by_discord_user_id(interaction.user.id)
        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!',
                                  description='Ваш аккаунт Discord не привязан к SS14.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
        ckey = await ss14.get_ckey(user_id)

    embeds = await get_all_char(user_id)
    if embeds is not None:
        title = f'# Персонажи {ckey}:'
        await interaction.followup.send(content=title, embeds=tuple(embeds))
    else:
        embed = discord.Embed(color=0xee0000, title=f'Пользователь {ckey} не имеет персонажей.',
                              description='[☉﹏☉]')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name='promo', description=promo_description, nsfw=False)
@app_commands.describe(ckey='C-key', code='Промокод')
async def promo(interaction: discord.Interaction, ckey: str | None, code: str):
    channel = interaction.channel

    user = interaction.user

    if ckey is not None:
        ckey = ckey.replace(' ', '')

        user_id = await get_user_id(ckey)

        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
    else:
        user_id = await get_user_id_by_discord_user_id(interaction.user.id)
        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!',
                                  description='Ваш аккаунт Discord не привязан к SS14.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
        ckey = await ss14.get_ckey(user_id)

    footer_text = f'Ckey: {ckey}, Discord: {user.name}'

    success, title, description = await try_promo(user.id, user_id, code)
    color = 0x5c85d6 if success else 0xee0000

    embed = discord.Embed(color=color, title=title, description=description)
    embed.set_footer(text=footer_text)
    await channel.send(embed=embed)


@bot.tree.command(name='status', description=status_description, nsfw=False)
@app_commands.describe()
async def status(interaction: discord.Interaction):
    await interaction.response.defer()

    title, description, color = await get_status()
    embed = discord.Embed(color=color, title=title,
                          description=description)
    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed)


# Orientiks
@bot.tree.command(name='balance', description=balance_description, nsfw=False)
@app_commands.describe(ckey='C-key')
async def balance(interaction: discord.Interaction, ckey: str | None):
    await interaction.response.defer()

    if ckey is not None:
        ckey = ckey.replace(' ', '')

        user_id = await get_user_id(ckey)

        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
    else:
        user_id = await get_user_id_by_discord_user_id(interaction.user.id)
        if user_id is None:
            embed = discord.Embed(color=0xee0000, title='Ошибка!',
                                  description='Ваш аккаунт Discord не привязан к SS14.')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed)
            return
        ckey = await ss14.get_ckey(user_id)

    embed = discord.Embed(color=0x5c85d6, title=f'Баланс {ckey}:', description=await get_balance(user_id))
    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name='transfer', description=transfer_description, nsfw=False)
@app_commands.describe(ckey='C-key получателя', )
async def transfer(interaction: discord.Interaction, ckey: str, amount: int):
    await interaction.response.defer()

    ckey = ckey.replace(' ', '')

    recipient_user_id = await get_user_id(ckey)

    amount = int(amount)
    if amount <= 0:
        return 'Неверная сумма', False

    if recipient_user_id is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Получатель не найден.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    if await get_discord_user_id_by_user_id(recipient_user_id) is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Discord аккаунт получателя не привязан к '
                                                                           'SS14.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    sender_user_id = await get_user_id_by_discord_user_id(interaction.user.id)
    if sender_user_id is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Ваш аккаунт Discord не привязан к SS14.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    if await orientiks.get_balance(sender_user_id) < amount:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Недостаточно средств')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    await do_transfer(sender_user_id, recipient_user_id, amount)

    embed = discord.Embed(color=0x5c85d6, title=f'Перевод совершен успешно!',
                          description=f'Баланс {ckey}: ' + await get_balance(recipient_user_id))
    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name='shop', description=shop_description, nsfw=False)
@app_commands.describe()
async def shop(interaction: discord.Interaction):
    await interaction.response.defer()

    user_id = await get_user_id_by_discord_user_id(interaction.user.id)
    if user_id is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Ваш аккаунт Discord не привязан к SS14.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    embed = discord.Embed(color=0x5c85d6, title='Товары, доступные к покупке:')
    button_manager = View()

    products = await get_products()

    def create_callback(product):
        async def buy(interaction: discord.Interaction):

            embed = discord.Embed(color=0xee0000, title='Опа', description='На данный момент магазин не доступен')
            embed.set_footer(text=debug_message, icon_url=debug_url)
            await interaction.followup.send(embed=embed, view=button_manager)
            return

            responding_user_id = await ss14.get_user_id_by_discord_user_id(interaction.USER.ID)

            button_manager.clear_items()

            if responding_user_id != user_id:
                embed = discord.Embed(color=0xee0000, title='Тихо!',
                                      description='Это не твой магазин')
                embed.set_footer(text=debug_message, icon_url=debug_url)
                await interaction.followup.send(embed=embed, view=button_manager)
                return

            if await orientiks.get_balance(responding_user_id) < product.price:
                embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Недостаточно средств.')
                embed.set_footer(text=debug_message, icon_url=debug_url)
                await interaction.response.edit_message(embed=embed, view=button_manager)
                return

            product_info = f'{product.description}\n**Цена:** {product.price} {product.price_tag}'
            embed = discord.Embed(color=0x5c85d6, title=f'Вы приобрели товар **{product.NAME}**:',
                                  description=product_info)

            await product.func(responding_user_id)
            await ss14.add_spent(responding_user_id, product.price)

            await interaction.response.edit_message(embed=embed, view=button_manager)

        return buy

    for i, product in enumerate(products):
        product_info = f'{product.description}\n**Цена:** {product.price} {product.price_tag}'
        embed.add_field(name=f"{product.emoji} {product.NAME}", inline=False, value=product_info)

        button = Button(label=product.NAME, row=i // 2, emoji=product.emoji)
        button.callback = create_callback(product)
        button_manager.add_item(button)

    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed, view=button_manager)


# Youtubers'
@bot.tree.command(name='profit', description='Выводит кол-во использований кода', nsfw=False)
@app_commands.describe(code='Код')
async def profit(interaction: discord.Interaction, code: str):
    await interaction.response.defer()

    code = code.replace(' ', '')

    if (not discord.utils.get(interaction.user.roles, id=Roles.youtuber)
            and interaction.user.id not in Private.admins
            and interaction.user.id != 574856443581300745):
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Недостаточно прав')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    profit_decs = await get_profit(code.lower())
    if not profit_decs:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный код не найден.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(color=0x5c85d6, title='Результат', description=profit_decs)
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)

    # Sponsors'


@bot.tree.command(name='change_color', description=change_color_description, nsfw=False)
@app_commands.describe(color='Цвет в формате HEX')
async def change_color(interaction: discord.Interaction, color: str):
    await interaction.response.defer()

    if '#' in color:
        color.replace('#', '')

    if len(color) != 6:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Неверное количество знаков в цвете.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    if not color.startswith('#') and len(color) in (4, 7) and all(c in '0123456789abcdef' for c in color):
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Некорректная запись цвета.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    user_id = await get_user_id_by_discord_user_id(interaction.user.id)
    if user_id is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Ваш аккаунт Discord не привязан к SS14.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    if SponsorData().get_info(user_id) is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Вы не спонсор.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    text = await change_ooc_color(UUID(user_id), color)
    embed = discord.Embed(color=0x5c85d6, title=f'Успех.',
                          description=text)
    await interaction.followup.send(embed=embed)


#  Admin's
@bot.tree.command(name='set_sponsor', description='Админская команда', nsfw=False)
@app_commands.describe(ckey='C-key', ooc_color='Цвет в OOC', tier='Тир')
async def boosty(interaction: discord.Interaction, ckey: str, ooc_color: str, tier: int, duration_in_days: int):
    await interaction.response.defer()

    ckey = ckey.replace(' ', '')

    if interaction.user.id not in Private.admins:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Недостаточно прав')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    user_id = await get_user_id(ckey)

    if user_id is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(color=0x5c85d6, title='Результат',
                              description=await set_sponsor(user_id, tier, timedelta(days=duration_in_days), ooc_color))
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name='add_time', description='Админская команда', nsfw=False)
@app_commands.describe(ckey='C-key', percent='Процент общего времени')
async def add_time(interaction: discord.Interaction, ckey: str, percent: float):
    await interaction.response.defer()

    ckey = ckey.replace(' ', '')

    if interaction.user.id not in Private.admins:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Недостаточно прав')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    user_id = await get_user_id(ckey)

    if user_id is None:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Указанный пользователь не найден.')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    desc = await add_all_time(user_id, percent)

    embed = discord.Embed(color=0x5c85d6, title='Результат', description=desc)
    embed.set_footer(text=debug_message, icon_url=debug_url)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name='fucking_reboot', description='Админская команда', nsfw=False)
@app_commands.describe()
async def add_time(interaction: discord.Interaction):
    await interaction.response.defer()

    if interaction.user.id not in Private.admins:
        embed = discord.Embed(color=0xee0000, title='Ошибка!', description='Недостаточно прав')
        embed.set_footer(text=debug_message, icon_url=debug_url)
        await interaction.followup.send(embed=embed)
        return

    embed = discord.Embed(color=0x5c85d6, title='Перезагрузка..', description='Но не факт что получится')
    await interaction.followup.send(embed=embed)
    os.system('shutdown -t 0 -r -f')


if __name__ == '__main__':
    bot.run(Bot.TOKEN)
