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
    data = "My data"
    address = pynunzen.generate_block_address(index, timestamp, parent, data)
    assert address == "86805876e6d6054e2b78bfda00ed0a44034d10b1ff7c359d31e3ff8d3e246be4"


def test_generate_genesis_block():
    block = pynunzen.generate_genesis_block()
    assert block.index == 1


def test_generate_new_block(blockchain):
    block = pynunzen.generate_new_block(blockchain, "Foo")
    assert block.index == 2
    assert block.parent == blockchain.end.address
    assert block.data == "Foo"
