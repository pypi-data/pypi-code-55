from enum import Enum
from hashlib import sha512, sha224

class AddressPrefix(Enum):
    GGO = 'GGO'
    MEASUREMENT = 'MEASUREMENT'
    SETTLEMENT = 'SETTLEMENT'
    

def generate_address(prefix: AddressPrefix, public_key: bytes) -> str:

    prefix_add = sha512(prefix.value.encode('utf-8')).digest()[:3]
    add = sha224(sha512(public_key).digest()).digest()
    checksum = sha512(sha512(prefix_add + add).digest()).digest()[:4]

    return (prefix_add + add + checksum).hex()







