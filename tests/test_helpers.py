#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pytz
import pytest


def test_utcts_fail():
    from pynunzen.helpers import utcts
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    mytz = pytz.timezone('Europe/Amsterdam')
    dt = mytz.normalize(mytz.localize(dt, is_dst=True))
    with pytest.raises(ValueError):
        utcts(dt)


def test_utcts():
    from pynunzen.helpers import utcts
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    utcts = utcts(dt)
    assert utcts == 1483272000


def test_double_hash256():
    from pynunzen.helpers import double_sha256
    value = "Foobar"
    hashed = double_sha256(value)
    assert hashed == "e501c5d9636166687cb24409f3a45684cf3722bf1f18bf485acd4f64635a09f0"


def test_double_hash256_None():
    from pynunzen.helpers import double_sha256
    value = None
    hashed = double_sha256(value)
    assert hashed == "cd372fb85148700fa88095e3492d3f9f5beb43e555e5ff26d95f5a6adc36f8e6"


def test_double_hash256_nonstring():
    from pynunzen.helpers import double_sha256
    value = 21
    hashed = double_sha256(value)
    assert hashed == "053b22ca1fcea7a8de0da76b0f4deaef4aa9fb1100bff13965c3c0da76272862"
