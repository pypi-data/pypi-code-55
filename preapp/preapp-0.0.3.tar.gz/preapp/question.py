from typing import Dict, Any, List
from abc import ABC
import json


class Question(ABC):
    def __init__(
        self, qtype: str, name: str, message: str, choices: List[str] = [], default: Any = None
    ):
        self.metadata = dict()
        self.metadata["type"] = qtype
        self.metadata["name"] = name
        self.metadata["message"] = message
        if len(choices) > 0:
            self.metadata["choices"] = choices
        if default != None:
            self.metadata["default"] = default

    def json(self) -> Dict[str, Any]:
        return self.metadata

    def name(self) -> str:
        return self.metadata["name"]


class ConfirmQuestion(Question):
    def __init__(self, name: str, message: str, default: bool):
        super(ConfirmQuestion, self).__init__("confirm", name, message, default=default)


class CheckboxQuestion(Question):
    def __init__(self, name: str, message: str, choices: List[str]):
        super(CheckboxQuestion, self).__init__(
            "checkbox", name, message, [{"name": choice} for choice in choices]
        )


class InputQuestion(Question):
    def __init__(self, name: str, message: str, default: str = ""):
        super(InputQuestion, self).__init__("input", name, message, default=default)


class ListQuestion(Question):
    def __init__(self, name: str, message: str, choices: List[str]):
        super(ListQuestion, self).__init__(
            "list", name, message, choices=[{"name": choice} for choice in choices], default=0
        )


class PasswordQuestion(Question):
    def __init__(self, name: str, message: str, default: str = ""):
        super(PasswordQuestion, self).__init__("password", name, message, default=default)
