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
