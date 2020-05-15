from . import provider, local_provider, s3_provider

PROVIDERS_MAP = {
    "s3": s3_provider.S3StorageProvider,
    "local": local_provider.LocalStorageProvider
}
"""Map provider names to implementations. Used in make_provider() factory
function."""


def make_provider(provider_type: str, **kwargs) -> provider.StorageProvider:
    """Make a StorageProvider from a provider type. Call with the arguments
    you would normally provide to the specific implementation's constructor.

    make_provider("azure", account_name="...", ...)

    Args:
        provider_type (str): The type of the provider. See PROVIDERS_MAP.
        **kwargs: The arguments for the provider implementation's constructor.

    Returns:
        StorageProvider: The provider of the given type.

    Raises:
        ValueError: If provider_type was invalid (i.e. not in PROVIDERS_MAP).
        TypeError: If the wrong arguments were given in kwargs.
    """
    try:
        return PROVIDERS_MAP[provider_type](**kwargs)
    except KeyError:
        raise ValueError(f"Invalid storage provider_type '{provider_type}'")