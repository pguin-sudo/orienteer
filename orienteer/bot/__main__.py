import sys
from datetime import datetime

from loguru import logger
from loguru_discord import DiscordSink

from disnake import Activity, ActivityType
from disnake.ext import commands

from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.bot.utils.extensions import Extensions
from orienteer.general.config.local import BOT_NAME, BOT_TOKEN, USERS_OWNERS, WEBHOOKS_LOGS, DEBUG_MODE

logger.add(DiscordSink(WEBHOOKS_LOGS['bot']))


class OrienteerBot(commands.InteractionBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = datetime.now()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    if not DEBUG_MODE:
        async def on_slash_command_error(self, interaction, *args, **kwargs):
            await interaction.edit_original_message(embed=embeds.error_message(Errors.unexpected_error.value, 'Пожалуйста, обратитесь к <@536086033050107914>, мы постараемся исправить её как можно скорее.'))
            logger.error(f"{interaction=}\n{args=}\n{kwargs=}")

    @property
    def start_time(self):
        return self._start


def main():
    bot = OrienteerBot(
        activity=Activity(name=BOT_NAME, type=ActivityType.playing),
        owner_ids=USERS_OWNERS
    )

    for e in Extensions.all():
        try:
            bot.load_extension(name=f"{e['package']}.{e['name']}")
            logger.success(f"Extension '{e['package']}.{e['name']}' loaded")
        except commands.ExtensionNotFound as e:
            logger.error(e)

    logger.info(f"Starting bot...")
    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
