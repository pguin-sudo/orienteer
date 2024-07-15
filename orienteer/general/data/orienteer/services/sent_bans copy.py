from typing import List
from sqlalchemy.orm import Session
from ..repositories.sent_bans import SentBanRepository


class SentBanCall:
    def __init__(self, session: Session):
        self.repository = SentBanRepository(session)

    def get_last_sent_ban(self):
        return self.repository.get_last_sent_ban()

    def get_last_sent_roleban(self):
        return self.repository.get_last_sent_roleban()

    def set_last_sent_ban(self, id: int):
        return self.repository.set_last_sent_ban(id)

    def set_last_sent_roleban(self, id: int):
        return self.repository.set_last_sent_roleban(id)
