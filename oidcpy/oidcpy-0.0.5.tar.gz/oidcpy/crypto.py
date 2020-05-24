import collections
import os


Keypair = collections.namedtuple('Keypair', 'private public')


def read_file(filename):
    with open(filename, "rb") as f:
        contents = f.read()
        return contents


def read_keys(private_key_path, public_key_path):
    """
      Read private and public key from PEM file on disk and return the contents
      in a namedtuple with `private` and `public` fields
    """
    if not os.path.exists(private_key_path):
        raise IOError(f"{private_key_path} not found or no permission to read")
    private_key = read_file(private_key_path)

    if not os.path.exists(public_key_path):
        raise IOError(f"{public_key_path} not found or no permission to read")
    public_key = read_file(public_key_path)

    return Keypair(private=private_key, public=public_key)
