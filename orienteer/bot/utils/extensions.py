class Extensions:
    __list__ = [
        {'package': 'orienteer.bot.cogs', 'name': 'common'},
        {'package': 'orienteer.bot.cogs', 'name': 'info'},
        {'package': 'orienteer.bot.cogs', 'name': 'promo'},
        {'package': 'orienteer.bot.cogs', 'name': 'orientiks'},
        {'package': 'orienteer.bot.cogs', 'name': 'sponsor'},
        {'package': 'orienteer.bot.cogs', 'name': 'owners'},
    ]

    @staticmethod
    def all():
        return Extensions.__list__

    @staticmethod
    def get(name):
        for e in Extensions.__list__:
            if e['name'] == name:
                return e
        else:
            return None

    def __repr__(self):
        return self.__list__.__repr__()
