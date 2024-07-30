import os
import asyncio
from fastapi import FastAPI

from loguru import logger
from loguru_discord import DiscordSink

from orienteer.api.utils.authentication import generate_link
from orienteer.api.routes import authentication, sponsors
from orienteer.general.config.local import WEBHOOKS_LOGS

logger.add(DiscordSink(WEBHOOKS_LOGS['api']))


app = FastAPI(template_dir=os.path.abspath('templates'))

app.include_router(authentication.router)
app.include_router(sponsors.router)

if __name__ == '__main__':
    link = asyncio.run(generate_link(
        'ffc80662-6c8d-4c67-a729-658717508eb1'))
    logger.info('Тестовая ссылка: ' + link, is_important=True)

    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
