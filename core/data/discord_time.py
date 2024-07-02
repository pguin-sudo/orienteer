import datetime


async def get_discord_datetime_tag(timestamp: datetime.datetime) -> str:
    return f'<t:{int(timestamp.timestamp())}:f>'


async def timedelta_to_russian_text(timedelta: datetime.timedelta) -> str:
    days, hours, minutes = timedelta.days, timedelta.seconds // 3600, timedelta.seconds % 3600 // 60
    days_string = '' if days == 0 else f'{int(days)} д.'
    hours_string = '' if hours == 0 else f', {int(hours)} ч.' if days > 0 else f'{int(hours)} ч.'
    min_string = '' if minutes == 0 else f', {int(minutes)} мин.' if hours > 0 else f'{int(minutes)} мин.'
    return days_string + hours_string + min_string
