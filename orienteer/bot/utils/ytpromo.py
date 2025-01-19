import disnake

def error_message(message: str) -> disnake.Embed:
    embed = disnake.Embed(title="Ошибка", description=message, color=disnake.Color.red())
    return embed
