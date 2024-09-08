from datetime import timedelta
from typing import Any
from uuid import UUID

from orienteer.general.formatting.playtime import get_job_group_and_name
from orienteer.general.formatting.time import get_formatted_timedelta
from ..repositories import playtime


async def get_formatted_grouped_trackers(user_id: UUID) -> list[str | Any]:
    playtimes = await playtime.get_all_trackers(user_id)

    groups = ["", "", "", "", "", "", "", "", "", "", ""]

    for _playtime in playtimes:
        if _playtime["tracker"] == "Overall":
            groups[10] = f"{get_formatted_timedelta(_playtime['time_spent'])}\n\n"
        else:
            name = get_job_group_and_name(_playtime["tracker"])
            groups[
                name[0]
            ] += (
                f"- **{name[1]}**: {get_formatted_timedelta(_playtime['time_spent'])}\n"
            )
    return groups


async def get_most_popular_role_name(user_id: UUID) -> str:
    popular_role = await playtime.get_most_popular_tracker(user_id)
    return (
        get_job_group_and_name(popular_role["tracker"])[1]
        if popular_role is not None
        else "Отсутствует"
    )


async def get_overall(user_id: UUID) -> timedelta:
    play_time = await playtime.get_playtime_timedelta(user_id, "Overall")
    return play_time if play_time is not None else timedelta()
