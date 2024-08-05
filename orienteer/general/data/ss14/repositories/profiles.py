from ..dbconnection import DBConnectionContextManager


async def get_profiles(preference) -> tuple:
    async with DBConnectionContextManager() as connection:
        profiles = await connection.fetch("SELECT * FROM profile WHERE preference_id = $1", preference)
        await connection.close()
        return tuple(profiles)
