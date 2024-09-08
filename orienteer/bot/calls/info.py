from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors, Results
from orienteer.general.config import CURRENCY_SIGN
from orienteer.general.data.orienteer.services import discord_auth, promo, sponsors, orientiks
from orienteer.general.data.requests import hub
from orienteer.general.data.ss14.services import player, playtime, bans, seen_time, admin_rank, whitelist, chars
from orienteer.general.formatting.player import ping
from orienteer.general.formatting.time import *


class Status(AbstractCall):
    async def __call__(self) -> None:
        server_data = await hub.find_server_data('ss14://amadis.orientacorp.ru:1313')

        if server_data is None:
            await self.interaction.edit_original_message(
                embed=embeds.result_message('Статус "Amadis ⚔️" - <:beer:1180521543390986324>:', '**Нет данных**',
                                            0xeb0c17))
            return

        preset = server_data["preset"]
        hidden_preset = preset if preset not in ('Ядерные оперативники', 'Предатели') else 'Секрет'

        text = (f'**Режим:** {hidden_preset}\n'
                f'**Игроки:** {server_data["players"]}/{server_data["soft_max_players"]}\n'
                f'**Раунд №** {server_data["round_id"]}')

        run_level = server_data['run_level']
        if run_level == 0:
            text += '\n**Загрузка раунда**'
            color = 0xbb61e8
        elif run_level == 1:
            time_string = server_data['round_start_time']

            given_time = datetime.strptime(time_string[:-9], '%Y-%m-%dT%H:%M:%S')
            current_time = datetime.now() + timedelta(hours=-3)

            time_difference = current_time - given_time

            text += f'\n**Продолжительность раунда:** {get_formatted_timedelta(time_difference)}'
            text += f'\n**Карта:** {server_data["map"]}'
            color = 0x5c85d6
        else:
            color = 0xeb0c17

        if server_data['panic_bunker']:
            text += '\n**Бункер**'
            color = 0xeb0c17

        await self.interaction.edit_original_message(
            embed=embeds.result_message('Статус "Amadis ⚔️" - <:nobeer:1180521621212114995>:', text, color))


class Roles(AbstractCall):
    async def __call__(self, ckey: str | None) -> None:
        if ckey is not None:
            ckey = ckey.replace(' ', '')

            user_id, ckey = await player.get_user_id_nocased(ckey)

            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_ckey.value))
                return
        else:
            user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
                return
            ckey = await player.get_ckey(user_id)

        all_roles = await playtime.get_formatted_grouped_trackers(user_id)
        if all_roles is None:
            embed = embeds.error_message(content=Errors.no_playtime_info.value)
            await self.interaction.edit_original_message(embed=embed)

        embed = embeds.result_message(f'Наигранное время {ckey}:', f'Общее: {all_roles[10]}')

        '' if all_roles[0] == '' else embed.add_field(name='Сервисный отдел:', value=all_roles[0], inline=False)
        '' if all_roles[1] == '' else embed.add_field(name='Инженерный отдел:', value=all_roles[1], inline=False)
        '' if all_roles[2] == '' else embed.add_field(name='Медицинский отдел:', value=all_roles[2], inline=False)
        '' if all_roles[3] == '' else embed.add_field(name='Служба безопасности:', value=all_roles[3], inline=False)
        '' if all_roles[4] == '' else embed.add_field(name='Отдел снабжения:', value=all_roles[4], inline=False)
        '' if all_roles[5] == '' else embed.add_field(name='Научный отдел:', value=all_roles[5], inline=False)
        '' if all_roles[6] == '' else embed.add_field(name='Синтеты:', value=all_roles[6], inline=False)
        '' if all_roles[7] == '' else embed.add_field(name='Отдел командования:', value=all_roles[7], inline=False)
        '' if all_roles[8] == '' else embed.add_field(name='ЦентКом:', value=all_roles[8], inline=False)
        '' if all_roles[9] == '' else embed.add_field(name='Другое:', value=all_roles[9], inline=False)

        await self.interaction.edit_original_message(embed=embed)


class Bans(AbstractCall):
    async def __call__(self, ckey: str | None) -> None:
        if ckey is not None:
            ckey = ckey.replace(' ', '')

            user_id, ckey = await player.get_user_id_nocased(ckey)

            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_ckey.value))
                return
        else:
            user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
                return
            ckey = await player.get_ckey(user_id)

        all_bans, total_time, total_fine = await bans.get_formatted_bans_and_total_stats(user_id)
        if all_bans is None:
            await self.interaction.edit_original_message(
                embed=embeds.result_message(content=Results.no_bans_info.value))
            return

        if len(all_bans) > 15:
            all_bans = all_bans[:-15]
            embed = embeds.result_message(f'Последние 15 банов игрока {ckey}:')
        else:
            embed = embeds.result_message(f'Баны игрока {ckey}:')

        for ban in all_bans:
            embed.add_field(ban[0], ban[1], inline=False)

        if total_fine > 0:
            embed.description = f'Итого со штрафов: -{total_fine} {CURRENCY_SIGN}\nСуммарное время банов: {get_formatted_timedelta(total_time)}'
        else:
            embed.description = 'Отсутствуют <:MF_Yelpozitiv:1198982508256165918>'
        await self.interaction.edit_original_message(embed=embed)


class Profile(AbstractCall):
    async def __call__(self, ckey: str | None) -> None:
        if ckey is not None:
            ckey = ckey.replace(' ', '')

            user_id, ckey = await player.get_user_id_nocased(ckey)

            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_ckey.value))
                return
            discord_user_id = await discord_auth.get_discord_user_id_by_user_id(user_id)
            if discord_user_id is None:
                ping_statement = 'Аккаунт не верифицирован 😶‍🌫️'
            else:
                ping_statement = f'Аккаунт верифицирован, как {ping(discord_user_id)} ✅'
        else:
            user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
                return
            ckey = await player.get_ckey(user_id)
            ping_statement = f'Аккаунт верифицирован, как {ping(self.interaction.user.id)} ✅'

        creator = await promo.get_creator_code(user_id)
        first_seen = await seen_time.get_formatted_first_seen_time(user_id)
        last_seen = await seen_time.get_formatted_last_seen_time(user_id)
        all_roles = await playtime.get_formatted_grouped_trackers(user_id)
        most_popular_role = await playtime.get_most_popular_role_name(user_id)
        sponsor_level, color = await sponsors.get_sponsor_status_and_color(user_id)

        a_rank = await admin_rank.get_admin_rank_name_and_time(user_id)

        is_in_whitelist = await whitelist.check_whitelist(user_id)
        balance_info = await orientiks.get_balance(user_id)
        ban_status = await bans.get_last_ban_status(user_id)

        embed = embeds.result_message(title=f'Профиль {ckey}:', content=f'Первое появление: {first_seen}\n'
                                                                        f'Последнее появление: {last_seen}')

        if color is None:
            if ban_status == 0:
                embed.color = 0x5c85d6
                ban_status = 'Без блокировки ✅'
            elif ban_status == 1:
                embed.colour = 0xe84f4f
                ban_status = 'Временно заблокирован 😶‍🌫️'
            elif ban_status == 2:
                embed.colour = 0x222222
                ban_status = 'Бессрочно заблокирован 🪦'
        else:
            if ban_status == 0:
                ban_status = 'Без блокировки ✅'
            elif ban_status == 1:
                ban_status = 'Временно заблокирован 😶‍🌫️'
            elif ban_status == 2:
                ban_status = 'Бессрочно заблокирован 🪦'
            embed.colour = color

        embed.add_field(name='Дискорд:', value=f'{ping_statement}', inline=False)
        embed.add_field(name='Статус:', value=f'{ban_status}', inline=False)
        if creator is not None:
            embed.add_field(name='Код пригласителя:', value=f'{creator}', inline=False)
        if all_roles is not None:
            embed.add_field(name='Наигранное время:', value=f'Общее: {all_roles[10]}', inline=False)
        if most_popular_role is not None:
            embed.add_field(name='Любимая роль:', value=f'{most_popular_role}', inline=False)
        if sponsor_level is not None:
            embed.add_field(name='Статус спонсора:', value=sponsor_level, inline=False)
        if a_rank is not None:
            embed.add_field(name='Ранг администратора:',
                            value=f'{a_rank[0]}, стаж: {get_formatted_timedelta(a_rank[1])}', inline=False)
        if is_in_whitelist:
            embed.add_field(name='Whitelist:', value='Есть! 😊', inline=False)
        else:
            embed.add_field(name='Whitelist:', value='Нет   <:EDGEHOG:1106583346835898399>', inline=False)
        if balance_info is not None:
            embed.add_field(name='Баланс:', value=f'{balance_info} {CURRENCY_SIGN}', inline=False)

        await self.interaction.edit_original_message(embed=embed)


class Chars(AbstractCall):
    async def __call__(self, ckey: str | None) -> None:
        if ckey is not None:
            ckey = ckey.replace(' ', '')

            user_id, ckey = await player.get_user_id_nocased(ckey)

            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_ckey.value))
                return
        else:
            user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
            if user_id is None:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
                return
            ckey = await player.get_ckey(user_id)

        all_chars = await chars.get_formatted_chars(user_id)
        if all_chars is None:
            await self.interaction.edit_original_message(
                embed=embeds.result_message(content=Results.no_bans_info.value))
            return

        embed_array = []
        for char in all_chars:
            embed_array.append(embeds.char_embed(*char))

        await self.interaction.edit_original_message(content=f'## Персонажи {ckey}', embeds=embed_array)
