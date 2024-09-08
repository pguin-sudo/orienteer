import asyncio
import time
from statistics import median
from uuid import UUID

from orienteer.general.config import POSTGRES_ORIENTEER_USER, POSTGRES_ORIENTEER_PASSWORD, POSTGRES_ORIENTEER_DBNAME
from orienteer.general.data.orienteer import database
from orienteer.general.data.orienteer.services import discord_auth

mocviu = UUID('ffc80662-6c8d-4c67-a729-658717508eb1')


async def orienteer_db_speed_test():
    elapsed_time_1 = []
    for i in range(10000):
        start = time.time()
        await discord_auth.get_discord_user_id_by_user_id(mocviu)
        elapsed_time_1.append(time.time() - start)

    database.database_helper = database.DatabaseHelper(
        (f'postgresql+asyncpg://{POSTGRES_ORIENTEER_USER}:{POSTGRES_ORIENTEER_PASSWORD}'
         f'@{'amadis.orientacorp.ru'}:{55432}/{POSTGRES_ORIENTEER_DBNAME}'), echo=False)
    elapsed_time_2 = []
    for i in range(10000):
        start = time.time()
        await discord_auth.get_discord_user_id_by_user_id(mocviu)
        elapsed_time_2.append(time.time() - start)

    print(f"""
    Тест времени обращения к базе данных (10000 запросов):
    Старый вариант: 
        - Сумма: {sum(elapsed_time_2)}c.
        - Среднее: {sum(elapsed_time_2)/10000}c.
        - Медиана: {median(elapsed_time_2)}c.
    Новый вариант:
        - Сумма: {sum(elapsed_time_1)}c.
        - Среднее: {sum(elapsed_time_1)/10000}c.
        - Медиана: {median(elapsed_time_1)}c.
    """)


asyncio.run(orienteer_db_speed_test())
