from __future__ import annotations

import sys
import traceback
from datetime import datetime
from loguru import logger

from disnake import Activity, ActivityType
from disnake.ext import commands

from orienteer.bot.utils.extensions import Extensions
from orienteer.general.config.local import BOT_NAME, BOT_TOKEN, USERS_OWNERS


class OrienteerBot(commands.InteractionBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = datetime.now()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_error(self, event, *args, **kwargs):
        logger.error(f"{event=}{args}{kwargs}")
        logger.error(f"{''.join(traceback.format_stack())}")

    @property
    def start_time(self):
        return self._start


def main():
    bot = OrienteerBot(
        activity=Activity(name=BOT_NAME, type=ActivityType.playing),
        owner_ids=USERS_OWNERS,
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
    try:
        if not sys.platform in ("win32", "cygwin", "cli"):
            import uvloop

            uvloop.install()
    except ImportError:
        logger.opt(lazy=True).info("Bot launch without speed extra.")
    main()
