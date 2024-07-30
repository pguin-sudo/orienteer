from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import promo


class Promo(commands.Cog):
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

        async with promo.Promo(interaction, True) as call:
            await call(code)


def setup(bot):
    bot.add_cog(Promo(bot))
