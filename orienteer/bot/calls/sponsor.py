from datetime import datetime, timezone

from g4f import Provider
from g4f.client import Client

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.data.orienteer.services import discord_auth, sponsors
from orienteer.general.data.ss14.services import player
from orienteer.general.formatting.time import get_formatted_datetime, get_formatted_timedelta


class SponsorInfo(AbstractCall):
    async def __call__(self) -> None:
        user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
        if user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
            return

        ckey = await player.get_ckey(user_id)

        sponsor = await sponsors.get_sponsor(user_id)
        color = None

        if sponsor is None:
            content = 'Данные о спонсорстве отсутствуют.'
        elif not sponsor.is_active:
            content = 'Привилегии временно деактивированы.'
        else:
            content = ''
            if sponsor.extra_slots != 0:
                content += f'- **Дополнительные слоты 🎰:** {sponsor.extra_slots}\n'
            if sponsor.ooc_color:
                content += f'- **Цвет в OOC 🧊:** #{sponsor.ooc_color}\n'
                color = int(sponsor.ooc_color, 16)
            if sponsor.allowed_markings:
                content += f'- **Модификации персонажа 😶‍🌫️:** {sponsor.allowed_markings}\n'
            if sponsor.ghost_theme:
                content += f'- **Тема призрака 👻:** {sponsor.ghost_theme}\n'
            if sponsor.have_sponsor_chat:
                content += f'- **Доступ в спонсор чат 💥**\n'
            if sponsor.have_priority_join:
                content += f'- **Приоритетный вход 🚪**\n\n'
            if sponsor.created_at:
                content += (f'*Первая подписка:* {get_formatted_datetime(sponsor.created_at)}, '
                            f'{get_formatted_timedelta(datetime.now(timezone.utc) - sponsor.created_at)} назад\n')

            if content == '':
                content = 'Нет активных привилегий.'

        await self.interaction.edit_original_message(
            embed=embeds.result_message(f'Подписки "{ckey}": ', content=content, color=color))


class SetColor(AbstractCall):
    async def __call__(self, color: str) -> None:
        user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
        if user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
            return

        sponsor = await sponsors.get_sponsor(user_id)

        if sponsor is None or sponsor.ooc_color is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.ooc_color_is_none.value))
            return

        if color is not None:
            color = color.lower()
            color = color.replace(' ', '')
            color = color.replace('#', '')
            if len(color) != 6:
                await self.interaction.edit_original_message(
                    embed=embeds.error_message(content=Errors.incorrect_color.value))
                return
            for digit in color:
                if digit not in '01234567890abcdef':
                    await self.interaction.edit_original_message(
                        embed=embeds.error_message(content=Errors.incorrect_color.value))
                    return

        await sponsors.set_colored_nick(user_id=user_id, color=color)

        await self.interaction.edit_original_message(
            embed=embeds.result_message(content=f'Цвет #{color} был установлен, как цвет ника'))


class Ask(AbstractCall):
    async def __call__(self, question: str) -> None:
        user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
        if user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_discord.value))
            return

        if not await sponsors.is_sponsor_active(user_id):
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.not_have_permissions.value))
            return

        client = Client()
        response = client.chat.completions.create(provider=Provider.HuggingChat, model="command-r+",
                                                  messages=[{'content': question}], )
        await self.interaction.edit_original_message(
            embed=embeds.result_message(title=question + '?', content=response.choices[0].message.content))
