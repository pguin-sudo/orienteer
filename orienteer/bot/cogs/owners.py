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


def setup(bot):
    bot.add_cog(Owners(bot))
