class MoreutilsError(ValueError):
    pass


class ConfigError(MoreutilsError):
    pass


class ConfigNotLoadedError(ConfigError):
    pass


class ConfigKeyError(ConfigError):
    pass
