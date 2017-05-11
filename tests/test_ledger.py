#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ledger
----------------------------------

Tests for `ledger` package.
"""

import pytest
import datetime

from pynunzen.helpers import utcts
from pynunzen.ledger.blockchain import (
    Blockchain,
    validate_block,
    generate_genesis_block,
    generate_new_block
)
from pynunzen.ledger.block import generate_block_address, __block_max_size__
from pynunzen.ledger.transaction import Transaction


@pytest.fixture
def blockchain():
    """Fixture for a empty blockchain."""
    return Blockchain()


@pytest.fixture
def transaction():
    """Fixture for a empty blockchain."""
    return Transaction()


@pytest.fixture
def blockchain_modified_genesis():
    """Fixture for a empty blockchain. And a modified genesis Block."""
    blockchain = Blockchain()
    genesis_block = blockchain.blocks[0]
    genesis_block.address = "hashismodified"
    blockchain.blocks[0] = genesis_block
    return blockchain


@pytest.fixture
def block_with_modified_genesis(blockchain_modified_genesis, transaction):
    """Fixture for a empty block."""
    return generate_new_block(blockchain_modified_genesis, [transaction, transaction, transaction])


@pytest.fixture
def block(blockchain, transaction):
    """Fixture for a empty block."""
    return generate_new_block(blockchain, [transaction, transaction, transaction])


def test_generate_block_address():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    index = 1
    timestamp = utcts(dt)
    parent = "parent"
    data = ["My data"]
    address = generate_block_address(index, timestamp, parent, data)
    assert address == "27edb13573987de43e061a400f89bbb10992b3b88c5356deaad2344ae2e77c6b"


def test_generate_genesis_block():
    block = generate_genesis_block()
    assert block.index == 0


def test_generate_new_block(blockchain, block, transaction):
    assert block.index == 1
    assert block.parent == blockchain.end.address
    assert block.data == [transaction, transaction, transaction]


def test_block_validation_ok(blockchain, block):
    result = validate_block(blockchain, block)
    assert result is True


def test_block_validation_modified_genesis(blockchain_modified_genesis,
                                           block_with_modified_genesis):
    with pytest.raises(ValueError):
        validate_block(blockchain_modified_genesis, block_with_modified_genesis)


def test_block_validation_fails_index(blockchain, block):
    block.index = 23
    with pytest.raises(ValueError):
        validate_block(blockchain, block)


def test_block_validation_fails_parent(blockchain, block):
    block.parent += "a"
    with pytest.raises(ValueError):
        validate_block(blockchain, block)


def test_block_validation_fails_address(blockchain, block):
    block.address += "a"
    with pytest.raises(ValueError):
        validate_block(blockchain, block)


def test_add_block(blockchain, block):
    blockchain.append(block)
    assert blockchain.length == 2


def test_add_block_fail(blockchain, block, transaction):
    fail_block = generate_new_block(blockchain, [transaction])
    blockchain.append(block)
    with pytest.raises(ValueError):
        blockchain.append(fail_block)


def test_wrong_block_data_container(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, "Foo")


def test_wrong_block_data_type(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, ["Foo"])


def test_max_size_block_data(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, [x for x in range(__block_max_size__ + 1)])


def test_min_size_block_data(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, [])
