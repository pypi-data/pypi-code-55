from typing import List


def parse_comma_list_message(message: str) -> List[str]:
    return [item.strip() for item in message.split(",")]
