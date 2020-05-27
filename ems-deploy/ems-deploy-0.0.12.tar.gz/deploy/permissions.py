import os
from deploy.chutils import check_permissions, symbolic_to_octal, check_ownership, extract_uid_gid, get_from_path

MOD_DEFAULT = "g+rwx"
OWN_DEFAULT = "root:iac-ems-dev"


def parse_permission(p: list):
    if p is None:
        mod = MOD_DEFAULT
        own = OWN_DEFAULT
    else:
        mod = p[0] if p[0] != "-" else MOD_DEFAULT
        own = p[1] if len(p) > 1 and p[1] != "-" else OWN_DEFAULT
    return mod, own


def check_permissions_and_ownership(input_map: dict, is_dir: bool):
    """
    Checks permissions and ownership. Input is a dict with path as key and a list or tuple as value with (chmod, chown)
    If the paths are directories (wit is_dir), it will try to create it if it doesn't exists.
    :param input_map: {<path>: (mod, chown)}
    :param is_dir: Whether the paths are directories
    """
    for d, p in input_map.items():

        try:
            mod, own = parse_permission(p)
        except Exception as e:
            print(f"Error parsing permissions for {d}={p}: {e}")
            continue

        # If directory, we create it if it doesn't exists
        if is_dir and not os.path.exists(d):
            if os.path.exists(d):
                try:
                    os.mkdir(d)
                except Exception as e:
                    print(f"Could not create directory {d}: {e}")
                    continue

        # Check ownership
        # Ownership is only supported on Linux/Mac
        if os.name != 'nt':
            if not check_ownership(d, own):
                try:
                    uid, gid = extract_uid_gid(own, d)
                    os.chown(d, uid, gid)
                except PermissionError:
                    print(f"Please set the right owner as root:\n\tchown -R {own} {d}")

        # Check permissions
        if not check_permissions(d, mod):
            try:
                os.chmod(d, symbolic_to_octal(mod, start=get_from_path(d)[0]))
            except PermissionError:
                print(f"Permissions are wrong - run (as root)\n\tchmod -R {mod} {d}")

