import datetime
import json
from uuid import UUID

from core.config import Cache


class SponsorData:
    def __init__(self):
        self.json_file = Cache.SPONSORS_DATA
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    # Get | Add | Delete

    def get_info(self, user_id) -> dict:
        return self.data.get(user_id, None)

    def add_info(self, user_id: UUID, tier: int, ooc_color: str, allowed_markings: tuple, ghost_theme: str,
                 expires_in: datetime.datetime):
        info = {
            "tier": tier,
            "oocColor": ooc_color,
            "havePriorityJoin": True,
            "extraSlots": tier,
            "allowedMarkings": allowed_markings,
            "ghostTheme": ghost_theme,
            "expiresIn": expires_in.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data[user_id] = info
        self.save_data()

    def delete_info(self, user_id: UUID):
        del self.data[user_id]
        self.save_data()

    # Others

    def get_tier(self, user_id: UUID):
        if user_id in self.data:
            return self.data[user_id].get("tier", None)
        else:
            return None

    def set_color(self, user_id: UUID, color):
        if user_id in self.data:
            self.data[user_id]["oocColor"] = color
            self.save_data()

    def get_color(self, user_id: UUID):
        if user_id in self.data:
            return self.data[user_id].get("oocColor", None)
        else:
            return None

    def set_expires_in(self, user_id: UUID, expires_in):
        if user_id in self.data:
            self.data[user_id]["expiresIn"] = expires_in.strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()

    def get_expires_in(self, user_id: UUID):
        if user_id in self.data:
            return datetime.datetime.strptime(self.data[user_id].get("expiresIn", None), "%Y-%m-%d %H:%M:%S")
        else:
            return None
