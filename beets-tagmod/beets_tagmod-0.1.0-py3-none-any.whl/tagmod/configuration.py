from typing import Any, Dict

from confuse import ConfigError, LazyConfig

CONFIGURATION_KEY_AUTOMATICALLY = "auto"
CONFIGURATION_KEY_MODIFICATIONS = "modifications"

DEFAULT_CONFIGURATION = {
    CONFIGURATION_KEY_AUTOMATICALLY: True,
    CONFIGURATION_KEY_MODIFICATIONS: {},
}


def _check_if_is_dict(obj: Any, obj_description: str) -> None:
    if not isinstance(obj, dict):
        raise ConfigError(
            f"{__name__}: '{obj_description}' is not a Dictionary!"
        )


def _check_if_is_string(obj: Any, obj_description: str) -> None:
    if not isinstance(obj, str):
        raise ConfigError(f"{__name__}: '{obj_description}' is not a String!")


def _verify_tag_modification(pattern: Any, replacement: Any) -> None:
    _check_if_is_string(pattern, f"pattern ['{pattern}']")
    _check_if_is_string(replacement, f"replacement ['{replacement}']")


def _verify_modification_entry(tag_name: Any, tag_modifications: Any) -> None:
    _check_if_is_string(tag_name, f"tag name ['{tag_name}']")
    _check_if_is_dict(tag_modifications, f"tag modifications ['{tag_name}']")

    for pattern, replacement in tag_modifications.items():
        _verify_tag_modification(pattern, replacement)


def _verify_modifications_entry(modifications: Any) -> None:
    _check_if_is_dict(modifications, CONFIGURATION_KEY_MODIFICATIONS)

    for tag_name, tag_modifications in modifications.items():
        _verify_modification_entry(tag_name, tag_modifications)


def set_default_configuration(configuration: LazyConfig) -> None:
    configuration.add(DEFAULT_CONFIGURATION)


def verify_configuration(configuration: LazyConfig) -> None:
    modifications = configuration[CONFIGURATION_KEY_MODIFICATIONS].get()
    _verify_modifications_entry(modifications)


def get_configured_modifications(
    configuration: LazyConfig,
) -> Dict[str, Dict[str, str]]:
    return configuration[CONFIGURATION_KEY_MODIFICATIONS].get()


def should_run_automatically(configuration: LazyConfig) -> bool:
    return configuration[CONFIGURATION_KEY_AUTOMATICALLY]
