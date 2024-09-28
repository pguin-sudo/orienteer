from disnake import CommandInteraction, Member
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import info
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.bot.utils.params import autocomplete_ckey
from orienteer.general.utils.dtos import UserDTO


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
    async def roles(self, interaction: CommandInteraction, discord: Member | None = None,
                    ckey: str | None = commands.Param(autocomplete=autocomplete_ckey, default=None)):
        """
        Выводит время, наигранное на разных ролях.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: ss14 ckey
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.no_user_id_with_discord.value))
                return
        if ckey and discord:
            await interaction.send(embed=embeds.error_message(Errors.ckey_and_discord.value))
            return
        user_dto = await UserDTO.from_ckey(ckey) if ckey else await UserDTO.from_discord_user_id(discord.id)
        if user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.unknown_user.value))
            return 

        async with info.Roles(interaction) as call:
            await call(user_dto)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def bans(self, interaction: CommandInteraction, discord: Member | None = None,
                   ckey: str | None = commands.Param(autocomplete=autocomplete_ckey, default=None)):
        """
        Выводит все полученные на сервере баны и общий штраф за них.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: ss14 ckey
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.no_user_id_with_discord.value))
                return
        if ckey and discord:
            await interaction.send(embed=embeds.error_message(Errors.ckey_and_discord.value))
            return
        user_dto = await UserDTO.from_ckey(ckey) if ckey else await UserDTO.from_discord_user_id(discord.id)
        if user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.unknown_user.value))
            return 

        async with info.Bans(interaction) as call:
            await call(user_dto)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def profile(self, interaction: CommandInteraction, discord: Member | None = None,
                      ckey: str | None = commands.Param(autocomplete=autocomplete_ckey, default=None), ):
        """
        Выводит  информацию, связанную с игровым аккаунтом.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: ss14 ckey
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.no_user_id_with_discord.value))
                return
        if ckey and discord:
            await interaction.send(embed=embeds.error_message(Errors.ckey_and_discord.value))
            return
        user_dto = await UserDTO.from_ckey(ckey) if ckey else await UserDTO.from_discord_user_id(discord.id)
        if user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.unknown_user.value))
            return 

        async with info.Profile(interaction) as call:
            await call(user_dto)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def chars(self, interaction: CommandInteraction, discord: Member | None = None,
                    ckey: str | None = commands.Param(autocomplete=autocomplete_ckey, default=None), ):
        """
        Выводит общую информацию о персонажах игрока.

        Parameters
        ----------
        interaction: Disnake interaction
        discord: ник в дискорд
        ckey: ss14 ckey
        """

        if not ckey and not discord:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto is None:
                await interaction.send(
                    embed=embeds.error_message(Errors.no_user_id_with_discord.value))
                return
        if ckey and discord:
            await interaction.send(embed=embeds.error_message(Errors.ckey_and_discord.value))
            return
        user_dto = await UserDTO.from_ckey(ckey) if ckey else await UserDTO.from_discord_user_id(discord.id)
        if user_dto is None:
            await interaction.send(embed=embeds.error_message(Errors.unknown_user.value))
            return 

        async with info.Chars(interaction) as call:
            await call(user_dto)


def setup(bot):
    bot.add_cog(Info(bot))
