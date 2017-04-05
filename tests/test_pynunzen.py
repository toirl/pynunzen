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
    assert address == "d93ce3d3e027e6f02c39e8aa332c7e0bc30df6bafb06a211cf7fa805aeb26702"


def test_generate_genesis_block():
    block = pynunzen.generate_genesis_block()
    assert block.index == 1


def test_generate_new_block(blockchain):
    block = pynunzen.generate_new_block(blockchain, "Foo")
    assert block.index == 2
    assert block.parent == blockchain.end.address
    assert block.data == "Foo"
