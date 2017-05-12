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


def test_send_fail_insufficient_output(coreA, coreB):
    from pynunzen.ledger.transaction import Coin
    # Get a address from coreA
    coreB_address = list(coreB.wallet.addresses.keys())[0]

    # Set 1000 from coreA to coreB
    with pytest.raises(ValueError):
        coreA.get_transaction(Coin(4001), coreB_address)


def test_get_transaction(coreA, coreB):
    from pynunzen.ledger.transaction import Coin
    # Get a address from coreA
    coreB_address = list(coreB.wallet.addresses.keys())[0]

    # Set 1000 from coreA to coreB
    tx = coreA.get_transaction(Coin(1001), coreB_address)

    # To settlte the requested amount of coins we need at least 2
    # inputs
    assert len(tx.inputs) == 4

    # The output should be two outputs.
    assert len(tx.outputs) == 2
    change = tx.outputs[0]
    spent = tx.outputs[1]
    assert spent[1].value == 1001
    assert change[1].value == 2999

    # Ensure that the change is readded to an address in out own wallet.
    assert change[0] in list(coreA.wallet.addresses.keys())
