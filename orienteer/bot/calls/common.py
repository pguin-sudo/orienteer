from disnake.ext.commands import Bot

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds


class Help(AbstractCall):
    async def __call__(self, bot: Bot):
        embed = embeds.result_message("Доступные команды:")

        for i, cog in enumerate(bot.cogs.values()):
            commands_str = ""
            commands = cog.get_slash_commands()
            for command in commands:
                commands_str += f"- /{command.name} - *{command.description}*\n"
            embed.add_field(
                name=f"{i+1}. {cog.description}", value=commands_str, inline=False
            )

        await self.interaction.edit_original_message(embed=embed)
