import datetime

from consistentor.rendezvous import rendezvous_hash


class Selector:
    def __init__(self, items=None):
        self.items = items if items else []

    def select_for_date(self, date: datetime.date = None):
        if not date:
            date = datetime.date.today()
        return rendezvous_hash(date.isoformat(), self.items)
