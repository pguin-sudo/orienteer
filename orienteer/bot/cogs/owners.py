from disnake import CommandInteraction, Member
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import owners
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.bot.utils.params import autocomplete_ckey, autocomplete_boosty_level
from orienteer.general.utils.dtos import UserDTO


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
        discord: Member | None = None,
        ckey: str = commands.Param(autocomplete=autocomplete_ckey),
    ):
        """
        Выдает указанное кол-во ориентиков определенному игроку.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: сикей
        amount: кол-во ориентиков
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.no_user_id_with_discord.value)
                )
                return
        elif ckey and discord:
            await interaction.send(
                embed=embeds.error_message(Errors.ckey_and_discord.value)
            )
            return
        elif ckey:
            user_dto = (
                await UserDTO.from_ckey(ckey)
            )
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.unknown_user.value)
                )
                return
        else:
            user_dto = (
                await UserDTO.from_discord_user_id(discord.id)
            )
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.unknown_user.value)
                )
                return

        async with owners.Reward(interaction) as call:
            await call(user_dto, amount)

    @commands.slash_command()
    @commands.is_owner()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def new_sponsor(
        self,
        interaction: CommandInteraction,
        discord: Member | None = None,
        ckey: str = commands.Param(autocomplete=autocomplete_ckey),
        boosty_level: str = commands.Param(autocomplete=autocomplete_boosty_level),
    ):
        """
        Выдает указанный уровень подписки определенному игроку.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: сикей
        boosty_level: уровень подписки на бусти
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.no_user_id_with_discord.value)
                )
                return
        elif ckey and discord:
            await interaction.send(
                embed=embeds.error_message(Errors.ckey_and_discord.value)
            )
            return
        elif ckey:
            user_dto = (
                await UserDTO.from_ckey(ckey)
            )
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.unknown_user.value)
                )
                return
        else:
            user_dto = (
                await UserDTO.from_discord_user_id(discord.id)
            )
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.unknown_user.value)
                )
                return

        async with owners.NewSponsor(interaction) as call:
            await call(user_dto, boosty_level)


def setup(bot):
    bot.add_cog(Owners(bot))
