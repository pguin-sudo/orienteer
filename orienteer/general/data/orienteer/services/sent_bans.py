from sqlalchemy.orm import Session

from ..models.sent_bans import SentBan


def create(self, last_sent_ban: int, last_seen_rolebans: int):
    new_entry = SentBan(last_sent_ban=last_sent_ban,
                        last_seen_rolebans=last_seen_rolebans)
    self.session.add(new_entry)
    self.session.commit()
    return new_entry


def get_last_sent_ban(self) -> int:
    return self.session.query(SentBan).first().last_sent_ban_id


def get_last_sent_roleban(self) -> int:
    return self.session.query(SentBan).first().last_sent_roleban_id


def set_last_sent_ban(self, id: int) -> SentBan | None:
    entry = self.self.session.query(SentBan)
    if entry:
        entry.last_sent_ban = id
        self.session.commit()
        return entry
    return None


def set_last_sent_roleban(self, id: int) -> SentBan | None:
    entry = self.self.session.query(SentBan)
    if entry:
        entry.last_sent_roleban = id
        self.session.commit()
        return entry
    return None
