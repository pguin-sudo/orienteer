from disnake.ext import commands
from disnake.ext.commands import Bot


class Owners(commands.Cog):
    """
    Приватные  🔒
    """

    def __init__(self, bot):
        self.bot: Bot = bot


def setup(bot):
    bot.add_cog(Owners(bot))
