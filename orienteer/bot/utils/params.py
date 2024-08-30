import disnake

from orienteer.general.data.products.services import boosty_levels
from orienteer.general.data.ss14.services import player


async def autocomplete_ckey(_: disnake.ApplicationCommandInteraction, user_input: str):
    return await player.contains_in_ckeys(user_input)


async def autocomplete_boosty_level(_: disnake.ApplicationCommandInteraction, user_input: str):
    ckeys = []
    for level in boosty_levels:
        if user_input.lower() in level.lower():
            ckeys.append(level)
            if len(ckeys) >= 20:
                break
    return ckeys
