from uuid import UUID

from orienteer.general.formatting.color import get_closest_color_name
from orienteer.general.formatting.time import get_years_form
from ..repositories import preferences, profiles


async def get_formatted_chars(user_id: UUID) -> tuple[tuple[str, str, int], ...]:
    preference = await preferences.get_preference(user_id)
    all_profiles = await profiles.get_profiles(preference)

    formatted = []
    for profile in all_profiles:
        if (
            profile["char_name"] is not None
            and profile["char_name"] != "поменяйте ник пожалуйста"
        ):
            title = f"**{profile['char_name']}**"
        else:
            title = "**Без имени**"

        if profile["species"] == "Moth":
            description = f"**Моль**"
        elif profile["species"] == "Human":
            description = f"**Человек**"
        elif profile["species"] == "Reptilian":
            description = f"**Унатх**"
        elif profile["species"] == "Vox":
            description = f"**Вокс**"
        elif profile["species"] == "Dwarf":
            description = f"**Дварф**"
        elif profile["species"] == "Felinid":
            description = f"**Фелинид**"
        elif profile["species"] == "Reptilian":
            description = f"**Унатх**"
        elif profile["species"] == "SlimePerson":
            description = f"**Слаймолюд**"
        elif profile["species"] == "HumanoidFoxes":
            description = f"**Вульпканин**"
        elif profile["species"] == "Oni":
            description = f"**Óни**"
        elif profile["species"] == "IPC":
            description = f"**КПБ**"
        else:
            description = f"{profile['species']}"

        description += f", {profile['age']} {get_years_form(profile['age'])}\n"

        if profile["sex"] == "Male":
            description += "**Мужчина**\n"
        elif profile["sex"] == "Female":
            description += "**Женщина**\n"
        else:
            description += "**Небинарная личность**\n"

        if profile["hair_name"] == "HairBald":
            description += f"**Лысый**\n"
        else:
            description += f"**Цвет волос:** {get_closest_color_name(profile['hair_color'][1:-2])}\n"

        if profile["facial_hair_name"] != "FacialHairShaved":
            description += f"**Цвет растительности:** {get_closest_color_name(profile['facial_hair_color'][1:-2])}\n"
        description += (
            f"**Цвет глаз:** {get_closest_color_name(profile['eye_color'][1:-2])}\n"
        )
        description += f"**Голос:** {str(profile['voice']).capitalize()}"

        formatted.append((title, description, int(profile["skin_color"][1:-2], 16)))

    return tuple(formatted)
