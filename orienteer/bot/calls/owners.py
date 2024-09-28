from datetime import timezone, datetime

import disnake

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.config import CURRENCY_SIGN
from orienteer.general.data.orienteer.services import (
    transactions,
    purchases,
)
from orienteer.general.data.products.services import boosty_levels
from orienteer.general.formatting import plots
from orienteer.general.formatting.player import ping
from orienteer.general.utils.dtos import UserDTO


class GOI(AbstractCall):
    async def __call__(self):
        embed = embeds.error_message(
            "Команда временно отключена",
            "Команда как бы есть, но её нет. В любом случае она обещала скоро вновь появиться...",
        )

        img_path = plots.plot_orientiks_cached_info(
            await transactions.get_cached_info_range()
        )
        last_cached_info = await transactions.get_cached_info_one(
            datetime.now(timezone.utc)
        )

        embed = embeds.success_message(
            f"Сводка о состоянии рынка ориентиков",
            f"**Спонсорские:** {last_cached_info.total_sponsorship} {CURRENCY_SIGN}\n"
            f"**Потраченные:** {last_cached_info.total_spent} {CURRENCY_SIGN}\n"
            f"**Штрафные:** {-last_cached_info.total_fine} {CURRENCY_SIGN}\n"
            f"**За наигранное время:** {last_cached_info.total_from_time - last_cached_info.total_time_balancing} {CURRENCY_SIGN}\n\n"
            f"**Итого:** {last_cached_info.total_from_time - last_cached_info.total_time_balancing - last_cached_info.total_fine + last_cached_info.total_sponsorship} {CURRENCY_SIGN}",
        )

        embed.timestamp = datetime.now(timezone.utc)
        embed.set_thumbnail(
            file=disnake.File(
                img_path, f"goi_{str(datetime.now(timezone.utc)).replace(' ', '_')}.png"
            )
        )

        await self.interaction.edit_original_message(embed=embed)


class Reward(AbstractCall):
    async def __call__(self, user_dto: UserDTO, amount: int):
        await transactions.add_orientiks_from_tip(user_dto.user_id, amount, "Reward")

        embed = embeds.success_message(
            content=f"{amount} ориентик(ов) были выданы {user_dto.ckey}{ping(user_dto.discord_user_id)}"
        )

        await self.interaction.edit_original_message(embed=embed)


class NewSponsor(AbstractCall):
    async def __call__(self, user_dto: UserDTO, subscription_level: str):
        for sponsor_product in boosty_levels[subscription_level]:
            await purchases.create_purchase(user_dto.user_id, sponsor_product.id, None)
            await sponsor_product.buy(user_dto.user_id)

        embed = embeds.success_message(
            content=f"Уровень подписки {subscription_level} был выдан {user_dto.ckey}{ping(user_dto.discord_user_id)}"
        )

        await self.interaction.edit_original_message(embed=embed)
