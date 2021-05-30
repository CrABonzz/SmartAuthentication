import hashlib
import os
import random

from Utils.common import DEFAULT_SALT_SIZE, GRID_PHOTOS


def random_salt(salt_size=DEFAULT_SALT_SIZE):
    return hashlib.sha256(os.urandom(salt_size)).hexdigest().encode('ascii')


def random_numbers(amount=1, max_number=len(GRID_PHOTOS)):
    return random.sample(range(max_number), amount)
