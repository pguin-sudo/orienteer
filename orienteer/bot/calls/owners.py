from datetime import timezone, datetime

import disnake

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds
from orienteer.general.data.orienteer.services import orientiks
from orienteer.general.formatting import plots


class GOI(AbstractCall):
    async def __call__(self):
        img_path = plots.plot_orientiks_cached_info(await orientiks.get_all_cached_info())
        last_cached_info = await orientiks.get_last_cached_info()

        embed = embeds.success_message(f'Сводка о состоянии рынка ориентиков',
                                       f'**Спонсорские:** {last_cached_info.total_sponsorship} <:orienta:1250903370894671963>\n'
                                       f'**Потраченные:** {last_cached_info.total_spent} <:orienta:1250903370894671963>\n'
                                       f'**Штрафные:** {-last_cached_info.total_fine} <:orienta:1250903370894671963>\n'
                                       f'**За наигранное время:** {last_cached_info.total_from_time - last_cached_info.total_time_balancing} <:orienta:1250903370894671963>\n\n'
                                       f'**Итого:** {last_cached_info.total_from_time - last_cached_info.total_time_balancing - last_cached_info.total_fine + last_cached_info.total_sponsorship} <:orienta:1250903370894671963>')

        embed.timestamp = datetime.now(timezone.utc)
        embed.set_thumbnail(file=disnake.File(img_path, f'goi_{str(datetime.now(timezone.utc)).replace(' ', '_')}.png'))

        await self.interaction.edit_original_message(embed=embed)
