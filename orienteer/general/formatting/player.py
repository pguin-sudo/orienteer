def ping(discord_user_id: int | None) -> str:
    return f'<@{str(discord_user_id)}>' if discord_user_id else ''


