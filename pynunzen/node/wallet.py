#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
import base64
from bitcoin import sha256, privtopub, pubtoaddr

from pynunzen.config import DEFAULT_WALLET_PATH

NBYTES_SECRET = 1024
"""Length of the random string (secret) in bytes used as the source for
building the private key"""


def generate_random():
    return os.urandom(NBYTES_SECRET)


def generate_key(seed):
    """Will generate a new keypair for public key encryption from the
    given seed. The keypair consists of a `private` and a `public` key.
    saved as a dictionary. The private key is used to sign and authorize
    transactions.  The `public` key is calculated from the private key
    using elliptic curve multiplication. The public key is used to
    receive transactions.

    Example::

        {
            'public':  '04ac8efbfd09fe097d843b2936...',
            'private': '40ba06385974e932bfefd922ca...',
        }

    :seed: Input which is used to generate the private key
    :returns: Keypair
    """
    private_key = sha256(seed)
    public_key = privtopub(private_key)
    return {"private": private_key, "public": public_key}


def read_keys(path):
    """Will read keys from the walletfile located under path""

    :path: Path to the wallet file
    :returns: Keys as list of dicts
    """
    with open(path) as walletfile:
        b_keys = walletfile.read()
    p_keys = base64.b64decode(b_keys)
    return pickle.loads(p_keys)


def write_keys(path, keys):
    """Will write the given keys in the walletfile located under path""

    :path: Path to the wallet file
    :keys: Keys as list of dicts
    """
    p_keys = pickle.dumps(keys)
    b_keys = base64.b64encode(p_keys)
    with open(path, "wb+") as walletfile:
        walletfile.write(b_keys)


class Wallet(object):
    """A wallet contains a collection of key pairs which are read and
    stored in a wallet file on the local filesystem. Each key pair
    consists of a private key and a public key. See
    :func:generate_key."""

    def __init__(self, path, number_keys=1):
        """Will initialize the wallet from walletfile located under
        path. If not existing a new wallet file will be created with an
        initial number for key pairs.

        :path: Path to the walletfile
        :number_keys: Number of key which are initialy generated when
        creating a new wallet
        """

        self.keyring = []
        if os.path.exists(path):
            self.keyring = read_keys(path)
        else:
            for n in range(number_keys):
                key = generate_key(generate_random())
                self.keyring.append(key)
            write_keys(path, self.keyring)

    @property
    def addresses(self):
        """Returns a mapping of addresses to related key pair.

        Example::

            {
                '1NcDeJ1JiXBrKrhk8wSbpkc1gFfSiPXY7a': {
                        'public':  '042a417d3a219a89c034828d14a...',
                        'private': '88884a59ad34106ac7550b87f59...'
                },
                '159XnH2sGZXbDPMfMkW5YkoZtEfKuvUtsV': {
                        'public':  '042a417d3a219a89c034828d14a...',
                        'private': '39928248766d1930bae8e421501...'
                },
                ...
            }

        :returns: Dictionary with address mapping
        """
        addresses = {}
        for key in self.keyring:
            address = pubtoaddr(key["public"])
            addresses[address] = key
        return addresses


if __name__ == "__main__":
    wallet = Wallet(path=DEFAULT_WALLET_PATH, number_keys=5)
    print(wallet.keyring)
    print(wallet.addresses)
