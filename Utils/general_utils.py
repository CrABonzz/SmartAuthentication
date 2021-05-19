import hashlib
import os

from Utils.common import DEFAULT_SALT_SIZE


def random_salt(salt_size=DEFAULT_SALT_SIZE):
    return hashlib.sha256(os.urandom(salt_size)).hexdigest().encode('ascii')
