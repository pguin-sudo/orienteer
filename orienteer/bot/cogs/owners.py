from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import owners
from orienteer.bot.utils.params import autocomplete_ckey, autocomplete_boosty_level


class Owners(commands.Cog):
    """
    Приватные  🔒
    """

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.is_owner()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def goi(self, interaction: CommandInteraction):
        """
        Global Orientiks Info.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        async with owners.GOI(interaction) as call:
            await call()

    @commands.slash_command()
    @commands.is_owner()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def reward(
        self,
        interaction: CommandInteraction,
        amount: int,
        ckey: str = commands.Param(autocomplete=autocomplete_ckey),
    ):
        """
        Выдает указанное кол-во ориентиков определенному игроку.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: сикей
        amount: кол-во ориентиков
        """

        async with owners.Reward(interaction) as call:
            await call(ckey, amount)

    @commands.slash_command()
    @commands.is_owner()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def new_sponsor(
        self,
        interaction: CommandInteraction,
        ckey: str = commands.Param(autocomplete=autocomplete_ckey),
        boosty_level: str = commands.Param(autocomplete=autocomplete_boosty_level),
    ):
        """
        Выдает указанный уровень подписки определенному игроку.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: сикей
        boosty_level: уровень подписки на бусти
        """

        async with owners.NewSponsor(interaction) as call:
            await call(ckey, boosty_level)


def setup(bot):
    bot.add_cog(Owners(bot))
