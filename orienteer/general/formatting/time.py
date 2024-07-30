from datetime import datetime, timedelta


def get_formatted_datetime(timestamp: datetime) -> str:
    return f'<t:{int(timestamp.timestamp())}:f>'


def get_formatted_timedelta(timedelta_: timedelta) -> str:
    days, hours, minutes = timedelta_.days, timedelta_.seconds // 3600, timedelta_.seconds % 3600 // 60
    days_string = '' if days == 0 else f'{int(days)} д.'
    hours_string = '' if hours == 0 else f', {int(hours)} ч.' if days > 0 else f'{int(hours)} ч.'
    min_string = '' if minutes == 0 else f', {int(minutes)} мин.' if hours > 0 else f'{int(minutes)} мин.'
    return days_string + hours_string + min_string


def get_years_form(number):
    if number % 10 == 1 and number % 100 != 11:
        return 'год'
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return 'года'
    else:
        return 'лет'
