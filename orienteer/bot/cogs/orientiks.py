from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import orientiks


class Orientiks(commands.Cog):
    """
    Экономика  💶
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def balance(self, interaction: CommandInteraction, ckey: str | None = None):
        """
        Выводит баланс ориентиков.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: ss14 ckey

        """

        async with orientiks.Balance(interaction) as call:
            await call(ckey)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def transfer(self, interaction: CommandInteraction, ckey: str, amount: int):
        """
        Перечисляет ориентики указанному пользователю.

        Parameters
        ----------
        interaction: Disnake interaction
        ckey: ss14 ckey получателя
        amount: количество переводимых ориентиков
        """

        async with orientiks.Transfer(interaction) as call:
            await call(ckey, int(amount))

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def shop(self, interaction: CommandInteraction):
        """
        Открывает магазин.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        async with orientiks.Shop(interaction) as call:
            await call()

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def purchases(self, interaction: CommandInteraction):
        """
        Выводит список всех купленных товаров.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        async with orientiks.Purchases(interaction) as call:
            await call()


def setup(bot):
    bot.add_cog(Orientiks(bot))
