from tracker_master.model.app_model import MonitoringName


class TemplateItem:

    def __init__(self, _id, name, key, status):
        self.id = _id
        self.name = name
        self.key = key
        self.status = status

    def is_active(self) -> bool:
        return self.status == 0


class HistoryItem:

    def __init__(self, _id, time, value):
        self.id = _id
        self.time = time
        self.value = value


class ZabbixItem:

    def __init__(self, _id, name, active):
        assert isinstance(name, MonitoringName)
        assert isinstance(active, bool)
        self.id = _id
        self.name = name
        self.active = active


class ZabbixTrigger:

    def __init__(self, _id, active, items=None):
        self.id = _id
        self.active = active
        self.items = items or list()


