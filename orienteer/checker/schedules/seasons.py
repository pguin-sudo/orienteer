from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from orienteer.general.config import WEBHOOKS_SEASONS, SEASON_MESSAGE_ID
from orienteer.general.data.orienteer.services import seasons, seasons_cached_playtime, discord_auth
from orienteer.general.data.products import products
from orienteer.general.data.ss14.services import player
from orienteer.general.formatting.time import get_formatted_timedelta
from orienteer.general.utils.discord import send_discord_message

USERNAME = 'Менеджер сезонов'


async def check_season_and_update():
    season = await seasons.get_current_season()
    leaderboard = await seasons_cached_playtime.get_leaderboard(season.season_id, depth=7)
    description = f'{season.description}\n'

    description += f'### Самые активные игроки:\n'
    for i, leader in enumerate(leaderboard):
        discord_user_id = await discord_auth.get_discord_user_id_by_user_id(leader[0])
        discord_ping = ' (<@' + str(discord_user_id) + '>)' if discord_user_id else ''
        description += f'{i + 1}. **{await player.get_ckey(leader[0])}{discord_ping}:** {get_formatted_timedelta(leader[1])}\n'

    description += f'### Награды:\n'
    for i, prize in enumerate(season.awards):
        description += f'{i + 1}. **{products.get_product(i).name}**\n'

    if not await send_discord_message(WEBHOOKS_SEASONS, USERNAME, title=season.title, description=description,
                                      color=int(season.color, 16), timestamp=datetime.now(timezone.utc),
                                      image_url=season.image_url, message_id=SEASON_MESSAGE_ID):
        logger.info('Leaderboard has not updated')

    logger.info('Leaderboard updated')


async def setup_seasons_schedule(scheduler: AsyncIOScheduler):
    await check_season_and_update()

    scheduler.add_job(check_season_and_update, CronTrigger(minute='*/10'))
