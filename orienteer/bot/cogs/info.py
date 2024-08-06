from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import info


class Info(commands.Cog):
    """
    Информация  ℹ️
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def status(self, interaction: CommandInteraction):
        """
        Выводит общую информацию о статусе сервера.

        Parameters
        ----------
        interaction: взаимодействие
        """

        async with info.Status(interaction) as call:
            await call()

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def roles(self, interaction: CommandInteraction, ckey: str | None = None):
        """
        Выводит время, наигранное на разных ролях.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: ss14 ckey
        """

        async with info.Roles(interaction) as call:
            await call(ckey)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def bans(self, interaction: CommandInteraction, ckey: str | None = None):
        """
        Выводит все полученные на сервере баны и общий штраф за них.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: ss14 ckey
        """

        async with info.Bans(interaction) as call:
            await call(ckey)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def profile(self, interaction: CommandInteraction, ckey: str | None = None):
        """
        Выводит  информацию, связанную с игровым аккаунтом.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: ss14 ckey
        """

        async with info.Profile(interaction) as call:
            await call(ckey)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def chars(self, interaction: CommandInteraction, ckey: str | None = None):
        """
        Выводит общую информацию о персонажах игрока.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: ss14 ckey
        """

        async with info.Chars(interaction) as call:
            await call(ckey)


def setup(bot):
    bot.add_cog(Info(bot))
