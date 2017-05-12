#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wallet
----------------------------------

Tests for `wallet` package.
"""

import os
from tempfile import gettempdir
import pytest


@pytest.fixture
def key():
    """Fixture for prefined key generated from the seed 'Insecure
    Seed'"""
    return {'public': '045195a66640f62fbd4c16c3621019e2a8ed5665c6399cf7d4214f2023d271516de3fccc23ec5caa250e352157d5ff390621b5ad1cc2e967d3b3d8caf504ee662d',
            'private': 'd05de875b2572f4092f51112e20a6177d4f3afcfd74c45cc55d6b55319c0f2a5'}


@pytest.fixture
def walletfile(key):
    from pynunzen.node.wallet import write_keys
    tmpdir = gettempdir()
    tmp_wallet = os.path.join(tmpdir, "testwallet.data")
    write_keys(tmp_wallet, [key])


@pytest.fixture
def newwallet():
    """Fixture for prefined key generated from the seed 'Insecure
    Seed'"""
    from pynunzen.node.wallet import Wallet
    tmpdir = gettempdir()
    tmp_wallet = os.path.join(tmpdir, "testwallet.data")
    if os.path.exists(tmp_wallet):
        os.remove(tmp_wallet)
    return Wallet(tmp_wallet)


@pytest.fixture
def wallet(walletfile):
    """Fixture for prefined key generated from the seed 'Insecure
    Seed'"""
    from pynunzen.node.wallet import Wallet
    tmpdir = gettempdir()
    tmp_wallet = os.path.join(tmpdir, "testwallet.data")
    return Wallet(tmp_wallet)

@pytest.fixture
def bob_wallet():
    """Fixture for prefined key generated from the seed 'Insecure
    Seed'"""
    from pynunzen.node.wallet import Wallet
    testdir = os.path.dirname(os.path.realpath(__file__))
    wallet_path = os.path.join(testdir, "bobwallet.data")
    return Wallet(wallet_path)

@pytest.fixture
def alice_wallet():
    """Fixture for prefined key generated from the seed 'Insecure
    Seed'"""
    from pynunzen.node.wallet import Wallet
    testdir = os.path.dirname(os.path.realpath(__file__))
    wallet_path = os.path.join(testdir, "alicewallet.data")
    return Wallet(wallet_path)


def test_generate_random():
    from pynunzen.node.wallet import NBYTES_SECRET, generate_random
    result = generate_random()
    assert len(result) == NBYTES_SECRET


def test_generate_random_unique():
    from pynunzen.node.wallet import generate_random
    result1 = generate_random()
    result2 = generate_random()
    assert result1 != result2


def test_generate_key(key):
    from pynunzen.node.wallet import generate_key
    nkey = generate_key("Insecure Seed")
    assert len(nkey.keys()) == 2
    assert nkey["public"] == key["public"]
    assert nkey["private"] == key["private"]


def test_wallet_creation(newwallet):
    assert len(newwallet.addresses) == 1


def test_wallet_address(wallet, key):
    addresses = wallet.addresses
    nkey = addresses["1Bv2uUhZCTFUsARCH812qwCBx8fKCJ88Du"]
    assert isinstance(nkey, dict)
    assert nkey["public"] == key["public"]
    assert nkey["private"] == key["private"]


def test_wallet_newaddress(newwallet):
    addresses = newwallet.addresses
    new_address = newwallet.get_new_address()
    assert len(addresses.keys()) < len(newwallet.addresses.keys())
    assert new_address in newwallet.addresses.keys()
