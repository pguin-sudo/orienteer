from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import common


class Common(commands.Cog):
    """
    Базовые 🏠
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def help(self, interaction: CommandInteraction):
        """
        Выводит список доступных команд.

        Parameters
        ----------
        interaction: взаимодействие
        """

        async with common.Help(interaction) as call:
            await call(self.bot)


def setup(bot):
    bot.add_cog(Common(bot))
