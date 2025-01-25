from disnake import CommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType
from orienteer.bot.utils import embeds
from orienteer.bot.utils.ytpromo import DropDownView
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.utils.dtos import UserDTO

class YouTubePromo(commands.Cog):
    """
    Промокоды с выбором отдела  🏆
    """

    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5.0, BucketType.user)
    async def ytpromo(self, interaction: CommandInteraction, code: str):
        """
        Использует промокод с выбором отдела.

        Parameters
        ----------
        interaction: Disnake interaction
        code: Промокод
        """
        ytpromo_code = code
        user_id = interaction.user.id

        user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
        if user_dto is None:
            await interaction.send(
                embed=embeds.error_message(Errors.no_user_id_with_discord.value)
            )
            return

        # Создаём выпадающий список после успешной проверки
        view = DropDownView(user_id, ytpromo_code)
        await interaction.response.send_message("Выберите ваш любимый отдел, к которому нужно добавить начальное время:", view=view, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(YouTubePromo(bot))
