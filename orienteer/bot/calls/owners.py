from datetime import timezone, datetime

import disnake

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.config import CURRENCY_SIGN
from orienteer.general.data.orienteer.services import orientiks, discord_auth, purchases
from orienteer.general.data.products.services import boosty_levels
from orienteer.general.data.ss14.services import player
from orienteer.general.formatting import plots
from orienteer.general.formatting.player import ping


class GOI(AbstractCall):
    async def __call__(self):
        img_path = plots.plot_orientiks_cached_info(await orientiks.get_all_cached_info())
        last_cached_info = await orientiks.get_cached_info(datetime.now(timezone.utc))

        embed = embeds.success_message(f'Сводка о состоянии рынка ориентиков',
                                       f'**Спонсорские:** {last_cached_info.total_sponsorship} {CURRENCY_SIGN}\n'
                                       f'**Потраченные:** {last_cached_info.total_spent} {CURRENCY_SIGN}\n'
                                       f'**Штрафные:** {-last_cached_info.total_fine} {CURRENCY_SIGN}\n'
                                       f'**За наигранное время:** {last_cached_info.total_from_time - last_cached_info.total_time_balancing} {CURRENCY_SIGN}\n\n'
                                       f'**Итого:** {last_cached_info.total_from_time - last_cached_info.total_time_balancing - last_cached_info.total_fine + last_cached_info.total_sponsorship} {CURRENCY_SIGN}')

        embed.timestamp = datetime.now(timezone.utc)
        embed.set_thumbnail(file=disnake.File(img_path, f'goi_{str(datetime.now(timezone.utc)).replace(' ', '_')}.png'))

        await self.interaction.edit_original_message(embed=embed)


class Reward(AbstractCall):
    async def __call__(self, ckey: str, amount: int):
        ckey = ckey.replace(' ', '')

        user_id, ckey = await player.get_user_id_nocased(ckey)

        if user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_ckey.value))
            return

        await orientiks.add_orientiks_from_sponsorship(user_id, amount)

        discord_user_id = await discord_auth.get_discord_user_id_by_user_id(user_id)

        embed = embeds.success_message(
            content=f'{amount} ориентик(ов) были выданы {ckey}{ping(discord_user_id)}')

        await self.interaction.edit_original_message(embed=embed)


class NewSponsor(AbstractCall):
    async def __call__(self, ckey: str, subscription_level: str):
        ckey = ckey.replace(' ', '')

        user_id, ckey = await player.get_user_id_nocased(ckey)

        if user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(content=Errors.no_user_id_with_ckey.value))
            return

        for sponsor_product in boosty_levels[subscription_level]:
            await purchases.create_purchase(user_id, sponsor_product.id, None)
            await sponsor_product.buy(user_id)

        discord_user_id = await discord_auth.get_discord_user_id_by_user_id(user_id)

        embed = embeds.success_message(
            content=f'Уровень подписки {subscription_level} был выдан {ckey}{ping(discord_user_id)}')

        await self.interaction.edit_original_message(embed=embed)
