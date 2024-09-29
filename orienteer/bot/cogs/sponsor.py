from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType

from orienteer.bot.calls import sponsor
from orienteer.bot.utils import embeds
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.utils.dtos import UserDTO


class Sponsors(commands.Cog):
    """
    Спонсорские  🎗️
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def sponsor_info(self, interaction: CommandInteraction):
        """
        Выводит информацию о спонсорских подписках.

        Parameters
        ----------
        interaction: Disnake interaction
        """

        async with sponsor.SponsorInfo(interaction) as call:
            await call()

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def set_color(
        self,
        interaction: CommandInteraction,
        color: str = commands.Param(min_length=6, max_length=6),
    ):
        """
        Меняет цвет спонсора.

        Parameters
        ----------
        interaction: Disnake interaction
        color: цвет
        """

        user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
        if user_dto is None:
            await interaction.send(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value)
            )

        async with sponsor.SetColor(interaction) as call:
            await call(user_dto, color)

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def ask(self, interaction: CommandInteraction, question: str):
        """
        Задает вопрос Всемогущему и Всесильному.

        Parameters
        ----------
        interaction: Disnake interaction
        question: вопрос
        """

        user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
        if user_dto is None:
            await interaction.send(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value)
            )

        async with sponsor.Ask(interaction) as call:
            await call(user_dto, question)


def setup(bot):
    bot.add_cog(Sponsors(bot))
