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


def test_utcts():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    utcts = pynunzen.utcts(dt)
    assert utcts == 1483272000

def test_utcts_fail():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    mytz = pytz.timezone('Europe/Amsterdam')             ## Set your timezone
    dt = mytz.normalize(mytz.localize(dt, is_dst=True))  ## Set is_dst accordingly
    with pytest.raises(ValueError):
        utcts = pynunzen.utcts(dt)


def test_generate_block_address():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    index = 1
    timestamp = pynunzen.utcts(dt)
    parent = "parent"
    data = "My data"
    address = pynunzen.generate_block_address(index, timestamp, parent, data)
    assert address == "7474c2d9971595ba2283d240b5696261921b0533f3000fef1f43861450d97a67"
