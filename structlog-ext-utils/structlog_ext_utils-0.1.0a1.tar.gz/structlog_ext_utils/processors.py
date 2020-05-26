from multiprocessing import current_process
from threading import current_thread


class VersionAppender:
    def __init__(self, number: str = "1", key: str = "@version"):
        self.number = str(number)
        self.key = key

    def __call__(self, _, __, event_dict):
        event_dict[self.key] = self.number
        return event_dict


class Application:
    def __init__(
        self, name, hostname, enable_thread: bool = False, enable_process: bool = False,
    ):
        self.name = name
        self.hostname = hostname
        self.enable_thread = enable_thread
        self.enable_process = enable_process

    def __call__(self, logger, method_name, event_dict):
        if self.enable_process:
            process_id, process_name = self.process_info()
            event_dict["process"] = {"id": process_id, "name": process_name}
        if self.enable_thread:
            thread_id, thread_name = self.thread_info()
            event_dict["thread"] = {"id": thread_id, "name": thread_name}
        event_dict["app_name"] = self.name
        event_dict["hostname"] = self.hostname
        return event_dict

    def process_info(self):
        process = current_process()
        return process.ident, process.name

    def thread_info(self) -> tuple:
        thread = current_thread()
        return thread.ident, thread.name


class RenameField:
    def __init__(self, fields: dict) -> None:
        self.fields = fields

    def __call__(self, _, __, event_dict):
        for from_key, to_key in self.fields.items():
            if event_dict.get(from_key):
                event_dict[to_key] = event_dict.pop(from_key)
        return event_dict
