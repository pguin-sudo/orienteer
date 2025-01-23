from disnake import CommandInteraction, SelectOption, MessageInteraction, ui
from disnake.ext import commands
from disnake.ext.commands import Bot, BucketType
from orienteer.bot.calls import ytpromo
from orienteer.bot.utils import embeds
# from orienteer.bot.utils.ytpromo import DropDownView
from orienteer.bot.utils.content_locale import Errors
from orienteer.general.data.orienteer.database import database_helper
from orienteer.general.utils.dtos import UserDTO

class Youtubelist(ui.StringSelect):
    def __init__(self, user_id: int, ytpromo_code: str):
        self.user_id = user_id  # Сохраняем ID пользователя
        self.ytpromo_code = ytpromo_code  # Сохраняем промокод
        self.selected_department = ""
        options = [
            SelectOption(label="Сервисный отдел", description="Время будет добавлено к ролям сервисного отдела", emoji="🍹"),
            SelectOption(label="Служба безопасности", description="Время будет добавлено к ролям службы безопасности", emoji="👮"),
            SelectOption(label="Медицинский отдел", description="Время будет добавлено к ролям медицинского отдела", emoji="🚑"),
            SelectOption(label="Инженерный отдел", description="Время будет добавлено к ролям инженерного отдела", emoji="🔧"),
            SelectOption(label="Научный отдел", description="Время будет добавлено к ролям научного отдела", emoji="🔬"),
            SelectOption(label="Отдел карго", description="Время будет добавлено к ролям отдела карго", emoji="📦"),
            SelectOption(label="Синтетики", description="Время будет добавлено к синтетикам", emoji="🤖"),
        ]

        super().__init__(placeholder="Выберите ваш любимый отдел", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: MessageInteraction):
        # Выбирать может только тот, кто вызвал. По идее защита от того, чтобы другие не выбирали, но всё равно видит только вызвавший
        if interaction.user.id != self.user_id:
            await interaction.response.edit_message("Вы не можете использовать этот промокод.", ephemeral=True)
            return

        # Сохраняем выбранный отдел и обрабатываем промокод
        self.selected_department = self.values[0]

        # Блокируем выбор после использования
        for item in self.view.children:
            if isinstance(item, ui.StringSelect):
                item.disabled = True  # Блокируем выпадающий список

        await interaction.response.edit_message(content="Проверка...", view=None)

        async with database_helper.session_factory() as db_session:
            user_dto = await UserDTO.from_discord_user_id(interaction.user.id)
            if user_dto:
                async with ytpromo.YoutubePromo(interaction, True) as call:
                    await call(user_dto, self.ytpromo_code, self.selected_department)

class DropDownView(ui.View):
    def __init__(self, user_id: int, ytpromo_code: str):
        super().__init__()
        self.add_item(Youtubelist(user_id, ytpromo_code))

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
