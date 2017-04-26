#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

TEST_VALUE = "Foo"
TEST_NONCE = "553F5ED82A079C7A"
TEST_HASH = "5236ebda5b2c2414f85c3249aa40bdf55b5b34d383314015d179310e582d058c"

def test_generate_hash():
    from pynunzen.ledger.pow import generate_hash
    hashvalue = generate_hash(TEST_VALUE, TEST_NONCE)
    assert hashvalue == TEST_HASH


def test_find_nonce():
    from pynunzen.ledger.pow import find_nonce, generate_hash
    find_nonce(TEST_VALUE, 2)
    # A sample nonce was saved in TEST_NONCE before.
    # hashvalue = generate_hash(value, TEST_NONCE)
    # This is saved in TEST_HASH


def test_verify_nonce():
    from pynunzen.ledger.pow import verify_hash
    assert verify_hash(TEST_HASH, 2) is True
