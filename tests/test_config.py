#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
----------------------------------

Tests for `config` module.
"""

import os
from tempfile import gettempdir

from pynunzen.config import get_config, get_node_server_address


def test_get_config_new():
    tmpdir = gettempdir()
    notexisting = "iamnothere"
    tmp_config = os.path.join(tmpdir, notexisting, "pynunzen.ini")
    config = get_config(tmp_config)
    assert config["peer"]["port"] == '7353'
    # Finally delete the file
    os.remove(tmp_config)
    os.removedirs(os.path.join(tmpdir, notexisting))


def test_get_config_existing():
    tmpdir = gettempdir()
    tmp_config = os.path.join(tmpdir, "pynunzen.ini")
    # First call will create the file
    config = get_config(tmp_config)
    # Second call will load the existing file again
    config = get_config(tmp_config)
    assert config["peer"]["port"] == '7353'
    # Finally delete the file
    os.remove(tmp_config)


def test_get_node_server_address():
    tmpdir = gettempdir()
    tmp_config = os.path.join(tmpdir, "pynunzen.ini")
    # First call will create the file
    config = get_config(tmp_config)
    address = get_node_server_address(config)
    assert address == "tcp://*:7353"
