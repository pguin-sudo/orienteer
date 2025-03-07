from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors, Results
from orienteer.general.data.orienteer.services import discord_auth, promo
from orienteer.general.utils.dtos import UserDTO


class Promo(AbstractCall):
    async def __call__(self, user_dto: UserDTO, code: str):
        if user_dto.user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value)
            )
            return

        success, content = await promo.try_promo(
            user_dto.user_id, code
        )

        await self.interaction.edit_original_message(
            embed=(
                embeds.success_message(Results.you_have_used_promo.value, content)
                if success
                else embeds.error_message(content=content)
            )
        )
