from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors, Results
from orienteer.general.data.orienteer.services import discord_auth, ytpromo
from orienteer.general.utils.dtos import UserDTO


class YoutubePromo(AbstractCall):
    async def __call__(self, user_dto: UserDTO, code: str, selected_department: str):
        if user_dto.user_id is None:
            await self.interaction.edit_original_message(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value)
            )
            return

        success, content = await ytpromo.try_ytpromo(user_dto.user_id, code, selected_department)

        await self.interaction.edit_original_message(
            embed=(
                embeds.success_message(Results.you_have_used_promo.value, content)
                if success
                else embeds.error_message(content=content)
            )
        )