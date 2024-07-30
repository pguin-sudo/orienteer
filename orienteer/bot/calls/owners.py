from g4f import Provider
from g4f.client import Client

from orienteer.bot.calls.abstract import AbstractCall
from orienteer.bot.utils import embeds


class Ask(AbstractCall):
    async def __call__(self, question: str) -> None:
        client = Client()
        response = client.chat.completions.create(provider=Provider.HuggingChat, model="command-r+",
                                                  messages=[{'content': question}], )
        await self.interaction.edit_original_message(
            embed=embeds.result_message(title=question + '?', content=response.choices[0].message.content))
