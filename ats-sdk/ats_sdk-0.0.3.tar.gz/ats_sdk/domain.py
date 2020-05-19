from enum import Enum


class TranslatableMessages(Enum):
    def __str__(self):
        return self.value
