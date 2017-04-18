#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_node
----------------------------------

Tests for `node` module.
"""

import pytest

from pynunzen.node.node import Node


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
