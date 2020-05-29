
import tarfile
from typing import Iterator, Optional, List, Tuple
import itertools
import re

from gpg_lite import GPGStore
import gpg_lite as gpg

from .dpkg import METADATA_FILE_SIG, METADATA_FILE


def fingerprint2keyid(fingerprint: str, keyid_len: int = 16) -> str:
    if len(fingerprint) < keyid_len:
        raise RuntimeError(f"Fingerpint must be at least {keyid_len} "
                           "characters long")
    return fingerprint[-keyid_len:]


def verify_metadata_signature(tar_file, gpg_store: GPGStore,
                              validation_keyid: Optional[str],
                              keyserver_url: str):
    """Check if the metadata file has been signed.

    :param tar_file: The tarfile containing a signature to check
    :param gpg_store: key database as gnupg object.
    :param validation_keyid: fingerprint of validation key (i.e. the key with
        which the input key(s) must be signed.
    :param keyserver_url: URL of keyserver from where the keys must originate.
    :raise RuntimeError: If the signature does not exist or is invalid
    """
    with tarfile.open(tar_file) as tar:
        try:
            sig = tar.extractfile(METADATA_FILE_SIG).read()
        except KeyError:
            raise RuntimeError(f"{tar_file}: Missing metadata signature")
        try:
            fpr = gpg_store.verify(tar.extractfile(METADATA_FILE), sig)
        except KeyError:
            raise RuntimeError(f"{tar_file}: Missing metadata")
        except gpg.cmd.GPGError as e:
            raise RuntimeError(
                f"{tar_file}: Metadata signature verification failed. {e}")

    next(validated_keys_by_ids((fingerprint2keyid(fpr),),
                               gpg_store,
                               validation_keyid,
                               keyserver_url))


def validated_keys_by_ids(key_ids: Iterator[str],
                          gpg_store: GPGStore,
                          validation_keyid: Optional[str],
                          keyserver_url: Optional[str] = None
                          ) -> Iterator[gpg.Key]:
    """Fetch keys for key_ids from store and validate

    This function performs the following tasks:
     - Download missing keys from the keyserver.
     - Refresh the keys used for encryption in the local keyring.
     - Validate keys.

    :param key_ids: ids of GnuPG keys to validate
    :param gpg_store: key database as gnupg object.
    :param validation_keyid: fingerprint of validation key (i.e. the key with
        which the input key(s) must be signed.
    :param keyserver_url: URL of keyserver from where the keys must originate.
    :return: Iterator with the validated keys.
    :raise RuntimeError: Raised if multiple keys are found for a given key_id.
    """
    key_ids = list(key_ids)
    keys = gpg_store.list_pub_keys(keys=key_ids, sigs=True)
    missing_keys = set(key_ids) - {k.key_id for k in keys} - \
        {subkey.key_id for key in keys for subkey in key.sub_keys}

    if len({k.key_id for k in keys}) + len(missing_keys) != len(set(key_ids)):
        raise RuntimeError(
            f"gpg corrupted: gpg returned a wrong number of keys "
            f"(ids: {', '.join(k.key_id for k in keys)}'."
            f"expected: {', '.join(set(key_ids) - missing_keys)}")
    keys = refresh_keys(keys=keys, gpg_store=gpg_store, sigs=True)
    if missing_keys:
        gpg_store.recv_keys(*missing_keys,
                            keyserver=keyserver_url)
        keys = itertools.chain(
            keys, gpg_store.list_pub_keys(keys=missing_keys, sigs=True))
    for key in keys:
        validate_pub_key(key, validation_keyid, keyserver_url)
        yield key


def refresh_keys(keys: List[gpg.Key],
                 gpg_store: GPGStore,
                 sigs: bool = True) -> List[gpg.Key]:
    """Refresh local copies of input keys by re-downloading them from the
    keyserver.

    :param gpg_store: local gpg keyring.
    :param keys: key(s) to refresh.
    :param sigs: if True, return keys with their signatures.
    :return: same list of keys as passed in input, but refreshed.
    :raise RuntimeError: If after refresh fingerprints do not match
    """
    # Group keys by their origin keyserver.
    urls_by_keys = {}
    for key in (key for key in keys if key.origin):
        urls_by_keys.setdefault(key.origin, []).append(key.fingerprint)

    # For each keyserver, re-download all keys that originally came from it.
    for url, keys_for_url in urls_by_keys.items():
        gpg_store.recv_keys(*keys_for_url, keyserver=url)

    # Reload all keys for local keyring. Note that since we base our search
    # keys on fingerprint, each search should always yield exactly one hit.
    fingerprints = [key.fingerprint for key in keys]
    refreshed_keys = {key.fingerprint: key for key in gpg_store.list_pub_keys(
        keys=fingerprints, sigs=sigs)}
    if set(fingerprints) != set(refreshed_keys):
        raise RuntimeError("Fingerprint mismatch after refresh. Before: " +
                           ", ".join(fingerprints) + "\nAfter: " +
                           ", ".join(refreshed_keys))
    return [refreshed_keys[fpr] for fpr in fingerprints]


def validate_pub_key(key: gpg.Key,
                     validation_keyid: Optional[str],
                     keyserver_url: Optional[str] = None) -> None:
    """Carries out checks on the GnuPG key passed as input.

    :param key: GnuPG key to validate.
    :param validation_keyid: fingerprint of validation key (i.e. the key with
        which the input key(s) must be signed.
    :param keyserver_url: URL of keyserver from where the keys must originate.
    :raises RuntimeError:
    """
    if key.validity is gpg.Validity.revoked:
        raise RuntimeError(f"{key.uids[0]} key has been revoked")
    if validation_keyid:
        assert_key_is_signed(key, sig_keyid=validation_keyid, sig_class='13x')
    if keyserver_url:
        assert_keyserver_origin_valid(key=key, keyserver=keyserver_url)


def assert_key_is_signed(key: gpg.Key,
                         sig_keyid: str,
                         sig_class: str = '13x') -> None:
    """Check that a GnuPG key is signed with the key specified by its key id
    (sig_keyid) and user id (sig_userid), and that the level of trust was set
    to sig_class.
    To do this we look at all signatures for the key, and check that at least
    one of them corresponds to the requested signature.
    Note: the 'sigs' key in the key object dictionary is a list of 3-tuple
    (keyid, user-id, signature-class).

    :param key: The key to check
    :param sig_keyid: key ID of the signee's key.
    :param sig_class: class/level of confidence the signee attributed to
        the key that has been signed. By default this value is set to '13x',
        which corresponds to the level:
            - Positive certification of a User ID and Public-Key packet. The
            issuer of this certification has done substantial verification of
            the claim of identity.
    :raises RuntimeError:
    """
    if not any((sig.issuer_key_id == sig_keyid and
                sig.signature_class == sig_class
                for sig in key.valid_signatures)):
        if any((sig.issuer_key_id == sig_keyid and
                sig.signature_class == sig_class
                for sig in key.signatures)):
            raise RuntimeError(f"{key.uids[0]} has a invalid or revoked signature "
                               f"by {sig_keyid}.")
        raise RuntimeError(f"{key.uids[0]} key is not signed. Only keys "
                           f"signed by {sig_keyid} are allowed to be used.")


def assert_keyserver_origin_valid(key: gpg.Key, keyserver: str):
    origin = key.origin
    if origin is None:
        return
    _, origin_hostname, origin_port = split_url(origin)
    _, keyserver_hostname, keyserver_port = split_url(keyserver)
    if origin_hostname != keyserver_hostname or (
            origin_port and keyserver_port and
            origin_port != keyserver_port):
        uid = key.uids[0]
        raise RuntimeError(f"The origin of key '{uid}' ({origin}) is not "
                           f"the keyserver specified in the config: {keyserver}")


def split_url(url: str) -> Tuple[Optional[str], str, Optional[str]]:
    """Similar to urllib.parse.urlparse, but also yields a hostname
    if there is no scheme
    """
    match = re.fullmatch(r"(https?://|hkp://)?([^:]+)(:[0-9]+)?", url)
    if not match:
        raise RuntimeError(f"Invalid URL: {url}")
    return match.groups()
