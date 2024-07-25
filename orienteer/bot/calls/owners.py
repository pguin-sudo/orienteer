from typing import Any

from g4f import Provider
from g4f.client import Client

from disnake import CommandInteraction
from datetime import datetime, timedelta

from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors

from orienteer.general.formatting.time import *

from orienteer.general.data.orienteer.services import promo, sponsors, orientiks
from orienteer.general.data.requests import hub
from orienteer.general.data.ss14.services import player, playtime, bans, seen_time, admin_rank, whitelist, chars

from orienteer.general.utils.calculations import calculate_fine

from .abstract import AbstractCall


class Ask(AbstractCall):
    async def __call__(self, question: str) -> None:
        client = Client()
        response = client.chat.completions.create(
            provider=Provider.HuggingChat,
            model="command-r+",
            messages=[{'content': question}],
        )
        await self.interaction.edit_original_message(embed=embeds.result_message(title=question+'?', content=response.choices[0].message.content))
