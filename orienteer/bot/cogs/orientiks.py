from disnake import CommandInteraction, Member
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import orientiks
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.bot.utils.params import autocomplete_ckey
from orienteer.general.utils.dtos import UserDTO


class Orientiks(commands.Cog):
    """
    Экономика  💶
    """

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def balance(self, interaction: CommandInteraction, discord: Member | None = None,
                      ckey: str | None = commands.Param(autocomplete=autocomplete_ckey, default=None)):
        """
        Выводит баланс ориентиков.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: ss14 ckey
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(embed=embeds.error_message(Errors.no_user_id_with_discord.value))
                return
        if ckey and discord:
            await interaction.send(embed=embeds.error_message(Errors.ckey_and_discord.value))
            return
        user_dto = await UserDTO.from_ckey(ckey) if ckey else await UserDTO.from_discord_user_id(discord.id)
        if user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.unknown_user.value))
            return

        async with orientiks.Balance(interaction) as call:
            await call(user_dto)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def transfer(self, interaction: CommandInteraction, amount: int, recipient_discord: Member | None = None,
                       recipient_ckey: str = commands.Param(autocomplete=autocomplete_ckey), ):
        """
        Перечисляет ориентики указанному пользователю.

        Parameters
        ----------
        interaction: Disnake interaction
        recipient_discord: ник в дискорд
        recipient_ckey: ss14 ckey получателя
        amount: количество переводимых ориентиков
        """

        if not recipient_ckey and not recipient_discord:
            await interaction.send(embed=embeds.error_message(Errors.no_ckey_or_discord.value))
            return
        if recipient_ckey and recipient_discord:
            await interaction.send(embed=embeds.error_message(Errors.ckey_and_discord.value))
            return
        recipient_user_dto = await UserDTO.from_ckey(
            recipient_ckey) if recipient_ckey else UserDTO.from_discord_user_id(recipient_discord.id)
        if recipient_user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.unknown_user.value))

        sender_user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
        if sender_user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.no_user_id_with_discord.value))
            return

        async with orientiks.Transfer(interaction) as call:
            await call(sender_user_dto, recipient_user_dto, int(amount))

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def shop(self, interaction: CommandInteraction):
        """
        Открывает магазин.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
        if user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.no_user_id_with_discord.value))

        async with orientiks.Shop(interaction) as call:
            await call(user_dto)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def purchases(self, interaction: CommandInteraction):
        """
        Выводит список всех купленных товаров.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        user_dto = await UserDTO.from_discord_user_id(interaction.user.id)

        async with orientiks.Purchases(interaction) as call:
            await call(user_dto)

    # @commands.slash_command()
    # @commands.cooldown(1, 5.0, BucketType.user)
    # async def buy(self, interaction: CommandInteraction, amount: int):
    #     """
    #     Позволяет покупать ориентики.
    #
    #     Parameters
    #     ----------
    #     interaction: Disnake interaction
    #     amount: количество покупаемых ориентиков
    #     """
    #
    #     async with orientiks.Buy(interaction) as call:
    #         await call(amount)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def bogachi(self, interaction: CommandInteraction):
        """
        Выводит список самых богатых людей.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        async with orientiks.Bogachi(interaction) as call:
            await call()


def setup(bot):
    bot.add_cog(Orientiks(bot))
