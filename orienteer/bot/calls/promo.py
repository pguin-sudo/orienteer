from typing import Any
from disnake import CommandInteraction
from datetime import datetime, timedelta

from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors, Results

from orienteer.general.formatting.time import *

from orienteer.general.data.orienteer.services import discord_auth, promo, sponsors, orientiks
from orienteer.general.data.requests import hub
from orienteer.general.data.ss14.services import player, playtime, bans, seen_time, admin_rank, whitelist, chars

from orienteer.general.utils.calculations import calculate_fine

from .abstract import AbstractCall


class Promo(AbstractCall):
    async def __call__(self, code: str):
        user_id = await discord_auth.get_user_id_by_discord_user_id(self.interaction.user.id)
        if user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value))
            return

        success, content = await promo.try_promo(self.interaction.user.id, user_id, code)

        await self.interaction.edit_original_message(embed=embeds.success_message(
            Results.you_have_used_promo.value, content) if success else embeds.error_message(content=content))
