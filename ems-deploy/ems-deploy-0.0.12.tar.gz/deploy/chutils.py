import os

g_offset = {
    "u": 1,
    "g": 4,
    "o": 7
}

p_index = {
    "r": 0,
    "w": 1,
    "x": 2
}


def bits(number):
    bit = 1
    while number >= bit:
        if number & bit:
            yield bit
        bit <<= 1


def parse_chmod(s: str, start="----------"):
    """
    Parses a chmod ddelta style string to a full chmod style string.
        >>> parse_chmod('go+rw,u+x')
        >>> '---xrw-rw-'
    One can also specify a start, to which the delta is applied
        >>> parse_chmod("a-w", start='---xrw-rw-')
        >>> '---xr--r--'
    If one supplies a full chmod style string, it just returns it
    :param s: Symbolic chmod string
    :param start: Initial symbolic chmod string
    :return: Resulting symbolic chmod string
    """
    k = list(start)

    if len(s) == 10 and "," not in s:
        k = list(s)
    else:
        for part in s.split(","):
            action = next(x for x in ["=", "-", "+"] if x in part)
            groups, bs = part.split(action)
            if not groups or groups == "a":
                groups = "ugo"
            for g in groups:
                for b in bs:
                    k[g_offset[g] + p_index[b]] = b if action != "-" else "-"

    return "".join(k)


def octal_to_symbolic(octal: int):
    """
    Transforms an octal representation to a full symbolic string
    :param octal: Octal representation (as integer)
    :return: Symbolic string
    """
    k = ""
    for idx, s in enumerate(["x", "w", "r"] * 3):
        if (octal >> idx) & 1:
            k = s + k
        else:
            k = "-" + k
    return "-" + k


def symbolic_to_octal(s, start="----------"):
    """
    Transforms a symbolic string to an octal representation. It accepts both delta an full. In case of a delta,
    an optional start-parameter can be supplied.
    :param s: Symbolic string
    :param start: Symblic string
    :return: Octal representation (integer)
    """
    k = parse_chmod(s, start)

    octal = "0" + "".join(["0" if x == "-" else "1" for x in k[1:]])

    return int(octal, base=2)


def get_from_path(path):
    """
    Extracts the permissions from a file at at specific path
    :param path: Path to the file
    :return: tuple with (symbolic,octal)
    """
    st = os.stat(path)
    oct_perm = st.st_mode & 0o777
    current = octal_to_symbolic(oct_perm)
    return current, oct_perm


def check_permissions(path, target):
    """
    Checks if the permissions of a file/directory match the target.
    :param path: Path to file/directory
    :param target: String - either a symbolic or octal representation
    :return: Boolean
    """
    current, oct_perm = get_from_path(path)

    if target.isnumeric():
        k = int(target, base=8)
    else:
        k = symbolic_to_octal(target, start=current)

    return oct_perm == k


def extract_uid_gid(owner_ship, defaultpath=None):
    import grp, pwd
    if ":" not in owner_ship:
        owner_ship += ":"

    uid = None
    gid = None
    if defaultpath:
        st = os.stat(defaultpath)
        uid = st.st_uid
        gid = st.st_gid

    n_uid, n_gid = owner_ship.split(":")

    if n_uid:
        try:
            uid = int(n_uid)
        except ValueError:
            uid = pwd.getpwnam(n_uid).pw_uid

    if n_gid:
        try:
            uid = int(n_gid)
        except ValueError:
            gid = grp.getgrnam(n_gid).gr_gid

    return uid, gid


def check_ownership(path, owner_ship):
    st = os.stat(path)
    uid = st.st_uid
    gid = st.st_gid

    t_uid, t_gid = extract_uid_gid(owner_ship, defaultpath=path)

    return t_uid == uid and t_gid == gid


if __name__ == "__main__":

    is_same = check_ownership("../test", "")
