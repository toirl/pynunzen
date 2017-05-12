#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_core
----------------------------------

Tests for `core` module.
"""
import pytest

from .test_wallet import alice_wallet, bob_wallet
from .test_ledger import blockchain


@pytest.fixture
def coreA(blockchain, alice_wallet):
    """Fixture for a empty blockchain."""
    from pynunzen.core import Core
    return Core(blockchain, alice_wallet)


@pytest.fixture
def coreB(blockchain, bob_wallet):
    """Fixture for a empty blockchain."""
    from pynunzen.core import Core
    return Core(blockchain, bob_wallet)


def test_core_init(coreA):
    from pynunzen.ledger.blockchain import Blockchain
    from pynunzen.node.wallet import Wallet
    assert isinstance(coreA.wallet, Wallet)
    assert isinstance(coreA.blockchain, Blockchain)


def test_balance_coreA(coreA):
    assert coreA.balance == 4000


def test_balance_coreB(coreB):
    assert coreB.balance == 6000

@pytest.mark.xfail
def test_send(coreA, coreB):
    from pynunzen.ledger.transaction import Coin
    # Get a address from coreA
    coreB_address = list(coreB.wallet.addresses.keys())[0]

    # Set 1000 from coreA to coreB
    tx = coreA.get_transaction(Coin(1000), coreB_address)
    #coreB.recv.set_transaction(tx)
