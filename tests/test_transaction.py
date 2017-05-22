#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_transaction
----------------------------------

Tests for `transaction` package.
"""

import pytest
from .test_ledger import blockchain
from .test_wallet import alice_wallet, bob_wallet


@pytest.fixture
def transaction(alice_wallet, bob_wallet, blockchain):
    """Fixture for a empty Transaction."""
    from pynunzen.ledger.transaction import Transaction, Input, Output, Coin, LockScript, UnlockScript
    senderaddress = list(alice_wallet.addresses)[0]
    receiveraddress = list(bob_wallet.addresses)[0]
    tx_in = Input(Coin(1000), UnlockScript(senderaddress), tx_hash=blockchain.blocks[1].data[0].hash, utxo_idx=0)
    tx_out1 = Output(Coin(999), LockScript(receiveraddress))
    tx_out2 = Output(Coin(0.5), LockScript(senderaddress))
    transaction = Transaction([tx_in], [tx_out1, tx_out2])
    return transaction


@pytest.fixture
def transaction_wrong_ref(alice_wallet, bob_wallet, blockchain):
    """Fixture for a empty Transaction."""
    from pynunzen.ledger.transaction import Transaction, Input, Output, Coin, LockScript, UnlockScript
    senderaddress = list(alice_wallet.addresses)[0]
    receiveraddress = list(bob_wallet.addresses)[0]
    tx_in = Input(Coin(1000), UnlockScript(senderaddress), tx_hash="1234" * 8, utxo_idx=0)
    tx_out1 = Output(Coin(999), LockScript(receiveraddress))
    tx_out2 = Output(Coin(0.5), LockScript(senderaddress))
    transaction = Transaction([tx_in], [tx_out1, tx_out2])
    return transaction


@pytest.fixture
def data_container():
    """Fixture for a empty Transaction."""
    from pynunzen.ledger.transaction import Data
    return Data("Foobar")


@pytest.fixture
def coin_container():
    """Fixture for a empty Transaction."""
    from pynunzen.ledger.transaction import Coin
    return Coin(0.0001)


def test_generate_hash(transaction_wrong_ref):
    from pynunzen.ledger.transaction import generate_transaction_hash
    transaction_wrong_ref.time = 1495142866
    assert generate_transaction_hash(transaction_wrong_ref) == "1511ce04090e426033a2ea906bc5e383a8c325ec806310fcf6023fca4552fa18"


def test_validate_transaction(transaction, blockchain):
    from pynunzen.ledger.transaction import validate_transaction
    assert validate_transaction(transaction, blockchain) is True


def test_validate_transaction_fails_ref(transaction_wrong_ref, blockchain):
    from pynunzen.ledger.transaction import validate_transaction
    assert validate_transaction(transaction_wrong_ref, blockchain) is False


def test_validate_transaction_fails_syn(transaction, blockchain):
    from pynunzen.ledger.transaction import validate_transaction
    transaction.foo = False
    assert validate_transaction(transaction, blockchain) is False


def test_check_syntax(transaction):
    from pynunzen.ledger.transaction import _check_syntax
    assert _check_syntax(transaction) is True


def test_check_syntax_fail(transaction):
    from pynunzen.ledger.transaction import _check_syntax
    transaction.foo = False
    assert _check_syntax(transaction) is False


def test_check_io(transaction):
    from pynunzen.ledger.transaction import _check_io
    assert _check_io(transaction) is True


def test_check_io_fail(transaction):
    from pynunzen.ledger.transaction import _check_io
    transaction.inputs = []
    assert _check_io(transaction) is False

def test_check_hash(transaction):
    from pynunzen.ledger.transaction import _check_hash
    assert _check_hash(transaction) is True

def test_check_hash_fail(transaction):
    from pynunzen.ledger.transaction import _check_hash
    transaction.hash = transaction.hash + "x"
    assert _check_hash(transaction) is False

def test_data_container_check(data_container):
    with pytest.raises(NotImplementedError):
        data_container.check("XXX")


def test_coin_container_check(coin_container):
    assert coin_container.check(0.01) is True


def test_coin_container_check_fail_type(coin_container):
    with pytest.raises(ValueError):
        coin_container.check("XXX")
