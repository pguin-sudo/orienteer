import disnake

from orienteer.general.data.ss14.services import player


async def autocomplete_ckey(inter: disnake.ApplicationCommandInteraction, user_input: str):
    return await player.contains_in_ckeys(user_input)
