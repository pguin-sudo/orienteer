from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from loguru import logger

from orienteer.general.config import WEBHOOKS_SEASONS, SEASON_MESSAGE_ID
from orienteer.general.data.orienteer.services import (
    seasons,
    seasons_cached_playtime,
    discord_auth,
)
from orienteer.general.data.products.services import get_product
from orienteer.general.data.ss14.repositories import playtime
from orienteer.general.data.ss14.services import player
from orienteer.general.formatting.time import get_formatted_timedelta, get_formatted_datetime
from orienteer.general.formatting.player import ping
from orienteer.general.formatting.time import get_formatted_timedelta
from orienteer.general.utils.discord import send_discord_message

USERNAME = "Менеджер сезонов"


async def setup_seasons_change(scheduler: AsyncIOScheduler):
    future_seasons = await seasons.get_seasons_after(datetime.now(timezone.utc))

    for i, season in enumerate(future_seasons[:-1]):
        if scheduler.get_job(f'end_season_{season.season_id}') is not None:
            continue

        retrieve_date = future_seasons[i+1]

        logger.debug(f'Scheduling change for Season ({season}) at '
                     f'{get_formatted_datetime(retrieve_date)}')

        async def season_change():
            leaderboard = await seasons_cached_playtime.get_leaderboard(7)
            for j in season.awards:
                await get_product(j).buy(leaderboard[j])

        scheduler.add_job(season_change(), DateTrigger(retrieve_date), args=[],
                          id=f'end_season_{season.season_id}', )


async def update_current_season():
    season = await seasons.get_season_by_date(datetime.now(timezone.utc))
    leaderboard = await seasons_cached_playtime.get_leaderboard(season.season_id, depth=7)
    description = f'{season.description}\n'

    description += f"### Самые активные игроки:\n"
    for i, leader in enumerate(leaderboard):
        discord_user_id = await discord_auth.get_discord_user_id_by_user_id(leader[0])
        description += (
            f"{i + 1}. **{await player.get_ckey(leader[0])}{ping(discord_user_id)}:** "
            f"{get_formatted_timedelta(leader[1])}\n"
        )

    description += f"### Награды:\n"
    for i, prize in enumerate(season.awards):
        description += f"{i + 1}. **{get_product(i).name}**\n"

    if not await send_discord_message(
        WEBHOOKS_SEASONS,
        USERNAME,
        title=season.title,
        description=description,
        color=int(season.color, 16),
        timestamp=datetime.now(timezone.utc),
        image_url=season.image_url,
        message_id=SEASON_MESSAGE_ID,
    ):
        logger.info("Leaderboard has not updated")

    logger.info("Leaderboard updated")


async def setup_seasons_schedule(scheduler: AsyncIOScheduler):
    scheduler.add_job(setup_seasons_change, CronTrigger(hour='*'), args=(scheduler,))

    await update_current_season()
    scheduler.add_job(update_current_season, CronTrigger(minute='*/10'))
