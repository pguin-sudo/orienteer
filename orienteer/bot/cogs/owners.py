from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import owners


class Owners(commands.Cog):
    """
    Приватные  🔒
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.is_owner()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def goi(self, interaction: CommandInteraction):
        """
        Global Orientiks Info

        Parameters
        ----------
        interaction: Disnake interaction
        """

        async with owners.GOI(interaction) as call:
            await call()


def setup(bot):
    bot.add_cog(Owners(bot))
