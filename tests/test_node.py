#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_node
----------------------------------

Tests for `node` module.
"""

import pytest
import datetime
from pynunzen.node.node import (
    Node, recv, MessageParseException,
    encode_json_msg, decode_json_msg
)


@pytest.fixture
def nodeA():
    """Fixture for a empty blockchain."""
    return Node("tcp://*:5555")


@pytest.fixture
def nodeB():
    """Fixture for a empty blockchain."""
    return Node("tcp://*:5556")


def test_node_init_address(nodeA):
    assert nodeA.address == "tcp://*:5555"


def test_node_init_peers(nodeA):
    assert nodeA.peers == []


def test_encode_message():
    msg = {}
    msg["success"] = True
    msg["type"] = "response"
    json_msg = encode_json_msg(msg)
    assert json_msg.find('"success": true') > -1


def test_encode_message_fail():
    with pytest.raises(MessageParseException):
        encode_json_msg("Foo")


def test_encode_message_fail2():
    with pytest.raises(MessageParseException):
        encode_json_msg({"Foo": datetime.datetime.now()})


def test_decode_message():
    msg = decode_json_msg('{"command": "Foo", "data": "Bar"}')
    assert msg["command"] == "Foo"
    assert msg["data"] == "Bar"


def test_decode_message_fail():
    with pytest.raises(MessageParseException):
        decode_json_msg("Foo")


def test_recv_unknown_command():
    with pytest.raises(MessageParseException):
        recv('{"command": "Foo", "data": "Bar"}')


def test_recv_ping_command():
    response = recv('{"command": "ping", "data": ""}')
    assert response.find('"success": true') > -1
