from uuid import UUID
from ..dbhandler import DBHandler


async def get_profiles(preference) -> tuple:
    async with DBHandler() as connection:
        profiles = await connection.fetch("SELECT * FROM profile WHERE preference_id = $1", preference)
        await connection.close()
        return profiles
