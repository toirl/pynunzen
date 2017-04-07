#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pynunzen
----------------------------------

Tests for `pynunzen` module.
"""

import pytest
import datetime
import pytz

from pynunzen import pynunzen


@pytest.fixture
def blockchain():
    """Fixture for a empty blockchain."""
    return pynunzen.Blockchain()


@pytest.fixture
def block(blockchain):
    """Fixture for a empty block."""
    return pynunzen.generate_new_block(blockchain, ["a", "b", "c"])


def test_utcts():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    utcts = pynunzen.utcts(dt)
    assert utcts == 1483272000


def test_utcts_fail():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    mytz = pytz.timezone('Europe/Amsterdam')
    dt = mytz.normalize(mytz.localize(dt, is_dst=True))
    with pytest.raises(ValueError):
        pynunzen.utcts(dt)


def test_generate_block_address():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    index = 1
    timestamp = pynunzen.utcts(dt)
    parent = "parent"
    data = ["My data"]
    address = pynunzen.generate_block_address(index, timestamp, parent, data)
    assert address == "27edb13573987de43e061a400f89bbb10992b3b88c5356deaad2344ae2e77c6b"


def test_generate_genesis_block():
    block = pynunzen.generate_genesis_block()
    assert block.index == 0


def test_generate_new_block(blockchain, block):
    assert block.index == 1
    assert block.parent == blockchain.end.address
    assert block.data == ["a", "b", "c"]


def test_block_validation_ok(blockchain, block):
    result = pynunzen.validate_block(blockchain, block)
    assert result is True


def test_block_validation_fails_index(blockchain, block):
    block.index = 23
    with pytest.raises(ValueError):
        pynunzen.validate_block(blockchain, block)


def test_block_validation_fails_parent(blockchain, block):
    block.parent += "a"
    with pytest.raises(ValueError):
        pynunzen.validate_block(blockchain, block)


def test_block_validation_fails_address(blockchain, block):
    block.address += "a"
    with pytest.raises(ValueError):
        pynunzen.validate_block(blockchain, block)


def test_add_block(blockchain, block):
    blockchain.append(block)
    assert blockchain.length == 2


def test_add_block_fail(blockchain, block):
    fail_block = pynunzen.generate_new_block(blockchain, ["Foo"])
    blockchain.append(block)
    with pytest.raises(ValueError):
        blockchain.append(fail_block)


def test_wrong_block_data(blockchain):
    with pytest.raises(ValueError):
        pynunzen.generate_new_block(blockchain, "Foo")
