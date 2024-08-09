from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd

from orienteer.general.data.orienteer.models.orientiks_cached_info import OrientiksCachedInfo


def plot_orientiks_cached_info(all_info: tuple[OrientiksCachedInfo, ...]) -> str:
    data = [info.__dict__ for info in all_info]
    df = pd.DataFrame(data,
                      columns=['date', 'total_sponsorship', 'total_friends', 'total_pardons', 'total_time_balancing',
                               'total_spent', 'total_fine', 'total_from_time'])

    # Create one big plot
    plt.figure(figsize=(14, 8))

    # Setting color
    plt.gcf().patch.set_facecolor('#2b2d31')
    plt.gcf().patch.set_edgecolor('#999')
    plt.gca().set_facecolor('#2b2d31')
    plt.gca().spines['top'].set_color('#999')
    plt.gca().spines['right'].set_color('#999')
    plt.gca().spines['left'].set_color('#999')
    plt.gca().spines['bottom'].set_color('#999')
    plt.gca().tick_params(axis='both', colors='#999')
    plt.grid(True, color='#999')

    # Plot each column
    plt.plot(df['date'], df['total_sponsorship'], marker='o', label='Спонсорские', color=(1, 1, 0.3, 1))
    plt.plot(df['date'], df['total_spent'], marker='o', label='Потраченные', color=(1, 0.3, 1, 1))
    plt.plot(df['date'], -df['total_fine'], marker='o', label='Штрафные', color=(1, 0.3, 0.3, 1))
    plt.plot(df['date'], df['total_from_time'] - df['total_time_balancing'], marker='o', label='За наигранное время',
             color=(0.3, 1, 0.3, 1))

    plt.plot(df['date'],
             df['total_from_time'] - df['total_time_balancing'] - df['total_fine'] + df['total_sponsorship'],
             marker='o', label='Общее', color=(1, 1, 1, 1))

    plt.title('Сводка о состоянии рынка ориентиков', color='white')
    plt.xlabel('Дата', color='white')
    plt.ylabel('Кол-во', color='white')
    plt.legend(loc='lower left')

    plt.tight_layout()

    bio = BytesIO()
    plt.savefig(bio, dpi=250, format='png')

    plt.close(plt.gcf())
    plt.clf()

    with open('cache/plot.png', 'wb') as f:
        f.write(bio.getvalue())

    return 'cache/plot.png'
