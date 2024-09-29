from typing import Optional
from uuid import UUID

from orienteer.general.data.orienteer.services import discord_auth
from orienteer.general.data.ss14.services import player


class UserDTO:
    user_id = UUID(int=0)
    ckey = ""
    discord_user_id: int | None = 0

    @classmethod
    async def from_user_id(cls, user_id: UUID) -> Optional["UserDTO"]:
        self = cls()
        self.ckey = await player.get_ckey(user_id)
        if self.ckey is None:
            return None
        self.user_id = user_id
        self.discord_user_id = await discord_auth.get_discord_user_id_by_user_id(
            self.user_id
        )
        return self

    @classmethod
    async def from_ckey(cls, ckey_nocased: str) -> Optional["UserDTO"]:
        self = cls()
        self.user_id, self.ckey = await player.get_user_id_nocased(ckey_nocased)
        if self.user_id is None:
            return None
        self.discord_user_id = await discord_auth.get_discord_user_id_by_user_id(
            self.user_id
        )
        return self

    @classmethod
    async def from_discord_user_id(cls, discord_user_id: int) -> Optional["UserDTO"]:
        self = cls()
        self.user_id = await discord_auth.get_user_id_by_discord_user_id(
            discord_user_id
        )
        if self.user_id is None:
            return None
        self.discord_user_id = discord_user_id
        self.ckey = await player.get_ckey(self.user_id)
        return self
