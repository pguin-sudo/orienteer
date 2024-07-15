from typing import Any
from loguru import logger
from disnake import CommandInteraction, InteractionResponseType


class AbstractCall():
    def __init__(self, interaction: CommandInteraction, ephemeral=False) -> None:
        self.interaction = interaction
        self.ephemeral = ephemeral

    async def __aenter__(self):
        if not self.interaction.response.is_done():
            await self.interaction.response.defer(ephemeral=self.ephemeral)
        return self

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if True:
            logger.info(
                f'Command "{self.__class__.__name__}" has been finished')
        else:
            logger.info(
                f'Command "{self.__class__.__name__}" has not been finished')
