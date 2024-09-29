from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import promo
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.utils.dtos import UserDTO


class Promo(commands.Cog):
    """
    Промокоды  🏆
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def promo(self, interaction: CommandInteraction, code: str):
        """
        Использует промокод.

        Parameters
        ----------
        interaction: Disnake interaction
        code: Промокод
        """

        user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
        if user_dto is None:
            await interaction.send(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value)
            )

        async with promo.Promo(interaction, True) as call:
            await call(user_dto, code)


def setup(bot):
    bot.add_cog(Promo(bot))
