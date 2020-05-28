from hashlib import md5
from uuid import UUID


def custom_uuid(id: int) -> str:
    return str(UUID(md5(str(id).encode("utf-8")).hexdigest()))


def random_sku(id: int) -> str:
    return md5(str(id).encode("utf-8")).hexdigest()[:8]
