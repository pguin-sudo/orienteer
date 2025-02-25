import asyncio
import os
from uuid import UUID

from fastapi import FastAPI
from loguru import logger
from loguru_discord import DiscordSink

from orienteer.api.routes import authentication, playtime, sponsors, purchases
from orienteer.api.utils.authentication import generate_link
from orienteer.general.config import WEBHOOKS_LOGS

if WEBHOOKS_LOGS["api"] is not None:
    logger.add(DiscordSink(WEBHOOKS_LOGS["api"]))

app = FastAPI(template_dir=os.path.abspath("templates"))

app.include_router(authentication.router)
app.include_router(sponsors.router)
app.include_router(playtime.router)
app.include_router(purchases.router)

if __name__ == "__main__":
    logger.success("<<<<<<<<<<<<<<<< API module is starting >>>>>>>>>>>>>>>>")

    link = asyncio.run(generate_link(UUID("ffc80662-6c8d-4c67-a729-658717508eb1")))
    logger.info("Тестовая ссылка: " + link, is_important=True)

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
