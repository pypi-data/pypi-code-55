"""request password from the user.
"""

import hashlib
import getpass

__version__="5.1" #VERSION#

# pylint: disable=invalid-name

def password_to_hash(pw):
    """convert a string to a md5 hash."""
    m= hashlib.md5()
    m.update(pw)
    return m.hexdigest()

def define_password():
    """ask the user to specify a password interactively."""
    p1= getpass.getpass("Please enter the password: ")
    p1= p1.strip()
    p2= getpass.getpass("Please re-enter          : ")
    p2= p2.strip()
    if p1 != p2:
        print("the passwords are unequal")
        return None
    return password_to_hash(p1)
