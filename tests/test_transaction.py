#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_transaction
----------------------------------

Tests for `transaction` package.
"""

import pytest


@pytest.fixture
def transaction():
    """Fixture for a empty Transaction."""
    from pynunzen.ledger.transaction import Transaction
    transaction = Transaction()
    transaction.inputs.append(1)
    transaction.outputs.append(2)
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


def test_validate_transaction(transaction):
    from pynunzen.ledger.transaction import validate_transaction
    assert validate_transaction(transaction) is True


def test_validate_transaction_fails(transaction):
    from pynunzen.ledger.transaction import validate_transaction
    transaction.foo = False
    assert validate_transaction(transaction) is False


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


def test_data_container_check(data_container):
    with pytest.raises(NotImplementedError):
        data_container.check("XXX")


def test_coin_container_check(coin_container):
    assert coin_container.check(0.01) is True


def test_coin_container_check_fail_type(coin_container):
    with pytest.raises(ValueError):
        coin_container.check("XXX")