from disnake import ui, SelectOption, MessageInteraction
from orienteer.general.data.orienteer.database import database_helper
from orienteer.general.utils.dtos import UserDTO
from orienteer.bot.calls import ytpromo

class Youtubelist(ui.StringSelect):
    def __init__(self, user_id: int, ytpromo_code: str):
        self.user_id = user_id
        self.ytpromo_code = ytpromo_code
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
        if interaction.user.id != self.user_id:
            await interaction.response.edit_message("Вы не можете использовать этот промокод.", ephemeral=True)
            return

        self.selected_department = self.values[0]

        for item in self.view.children:
            if isinstance(item, ui.StringSelect):
                item.disabled = True

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