from io import BytesIO

import matplotlib.pyplot as plt
import mplcyberpunk
import pandas as pd

from orienteer.general.data.orienteer.models.orientiks_cached_info import (
    OrientiksCachedInfo,
)


def plot_orientiks_cached_info(all_info: tuple[OrientiksCachedInfo, ...]) -> str:
    data = [info.__dict__ for info in all_info]
    df = pd.DataFrame(
        data,
        columns=[
            "date",
            "total_sponsorship",
            "total_friends",
            "total_pardons",
            "total_time_balancing",
            "total_spent",
            "total_fine",
            "total_from_time",
        ],
    )

    plt.gca().tick_params(axis="both")
    plt.grid(True)

    with plt.style.context("cyberpunk"):
        plt.figure(figsize=(14, 8))

        plt.plot(
            df["date"],
            df["total_sponsorship"],
            label="Спонсорские",
            color=(1, 1, 0.3, 1),
            lw=1,
            marker="",
            ms=20,
        )
        plt.plot(
            df["date"],
            df["total_spent"],
            label="Потраченные",
            color=(1, 0.3, 1, 1),
            lw=1,
            marker="",
            ms=20,
        )
        plt.plot(
            df["date"],
            -df["total_fine"],
            label="Штрафные",
            color=(1, 0.3, 0.3, 1),
            lw=1,
            marker="",
            ms=20,
        )
        plt.plot(
            df["date"],
            df["total_from_time"] - df["total_time_balancing"],
            label="За наигранное время",
            color=(0.3, 1, 0.3, 1),
            lw=1,
            marker="",
            ms=20,
        )

        plt.plot(
            df["date"],
            df["total_from_time"]
            - df["total_time_balancing"]
            - df["total_fine"]
            + df["total_sponsorship"],
            label="Общее",
            color=(1, 1, 1, 1),
            lw=2,
            marker="",
            ms=20,
        )

        plt.legend(loc="lower left")

        mplcyberpunk.make_lines_glow()
        mplcyberpunk.add_underglow(alpha_underglow=0.02)

        plt.title("Сводка о состоянии рынка ориентиков")
        plt.xlabel("Дата")
        plt.ylabel("Кол-во")

        bio = BytesIO()
        plt.savefig(bio, dpi=250, format="png")

        with open("cache/plot_orientiks_cached_info.png", "wb") as f:
            f.write(bio.getvalue())

        return "cache/plot_orientiks_cached_info.png"
