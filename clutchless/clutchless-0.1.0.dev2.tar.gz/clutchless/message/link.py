from typing import Sequence, Mapping


def print_incompletes(incompletes: Sequence[Mapping]):
    if len(incompletes) > 0:
        for item in incompletes:
            print(f'{item["name"]}')
