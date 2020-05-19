from typing import Dict

from ats_sdk.domain import TranslatableMessages


def fetch_translatable_strings(resource: Dict):
    if isinstance(resource, TranslatableMessages):
        yield str(resource)
    elif isinstance(resource, list):
        for val in resource:
            yield from fetch_translatable_strings(val)
    elif isinstance(resource, dict):
        for val in resource.values():
            yield from fetch_translatable_strings(val)


def translate(resource: Dict, translated_strings: Dict):
    def _translate(obj: dict):
        if isinstance(obj, TranslatableMessages):
            return translated_strings.get(str(obj))
        if isinstance(obj, list):
            return [_translate(val) for val in obj]
        if isinstance(obj, dict):
            return {k: _translate(v) for k, v in obj.items()}

        return obj

    return _translate(resource)
