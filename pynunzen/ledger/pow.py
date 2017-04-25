#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Proof of work This modul contains helper method used to to the proof
of work when generating blocks."""

import random
import logging
import time
from pynunzen.helpers import double_sha256


DIFFICULTY = 10
"""Number of trailing zero values in the generated hash"""

NONCE = ""
"""All the blocks in the Bitcoin block chain have a short string of
meaningless data—called a nonce attached to them. The mining computers
are required to search for the right meaningless string such that the
block as a whole satisfies a certain arbitrary condition. Specifically,
it is required that the SHA-256 hash of the block have a certain number
of trailing zeros
"""

POOL = "0123456789ABCDEF"

log = logging.getLogger(__name__)


def generate_nonce(pool, length=None):
    """Will return a random string build from the chars contained in the
    pool. The length of the string is the length of the pool on default.
    This string is used as nonce.

    :pool: Pool of chars which is used to build the nonce.
    :length: Length of the generated string.
    :returns: yield permutations

    """
    while 1:
        yield ''.join(random.choice(pool) for _ in range(len(pool)))


def find_nonce(value, difficulty, pool=POOL):
    """Will return a random nonce which matches the requirement that the
    generated hash of the concatenated value and nonce have a minimum
    number of leading zeros.

    :value: Static string, which is modified over and over again with generated nonce.
    :returns: nonce

    """
    cycle = 1
    for nonce in generate_nonce(pool):
        hashvalue = generate_hash(value, nonce)
        if verify_hash(hashvalue, difficulty):
            log.info("Found nonce with cycle {}".format(cycle))
            return nonce
        cycle += 1


def generate_hash(value, nonce):
    """Will generate a hash value form the concatenated value and nonce.

    :value: Static string, which is modified over and over again with the nonce.
    :nonce: Random data added to the value.
    :returns: A hash build from the given value and nonce

    """
    return double_sha256(value + nonce)


def verify_hash(hashvalue, difficulty):
    """Returns True if the given hash value has enough leading zeros in
    the binary representation of the given hash value. The number of
    required trailing zeros is defined by the given difficulty.

    :hashvalue: generated hash
    :difficulty: Number of leading zeros the generated has must have.
    :returns: True or False

    """
    pattern = "0" * difficulty
    binvalue = bin(int(hashvalue, 16))[2::]
    if binvalue.endswith(pattern):
        return True
    return False


if __name__ == "__main__":
    for difficulty in range(DIFFICULTY, 25):
        a = time.time()
        nonce = find_nonce("Hello World!", difficulty)
        b = time.time()
        print("Found after {} with difficulty {}".format((b - a), difficulty))
