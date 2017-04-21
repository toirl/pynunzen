#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_node
----------------------------------

Tests for `node` module.
"""

import pytest
from pynunzen.node.node import (
    Node, recv
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


def test_recv_unknown_command():
    with pytest.raises(RuntimeError):
        recv('{"command": "Foo", "data": "Bar", "mtype": "request"}')


def test_recv_ping_command():
    response = recv('{"command": "ping", "data": "", "mtype": "request"}')
    assert response.find('"success": true') > -1
