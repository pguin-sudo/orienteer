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
    async def ask(self, interaction: CommandInteraction, question: str):
        """
        Задает вопрос Всемогущему и Всесильному.

        Parameters
        ----------
        interaction: Disnake interaction
        question: вопрос
        """

        async with owners.Ask(interaction) as call:
            await call(question)


def setup(bot):
    bot.add_cog(Owners(bot))
