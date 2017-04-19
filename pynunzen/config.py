#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import configparser

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.pynunzen.ini")

DEFAULT_CONFIG = """
[server]
bind = *
# Listen for incoming request on all adresses
port = 7353
# Listen on this port. Default port is 7353

[peer]
host = localhost
# First connect to this host
port = ${server:port}
# Port to connect. Defaults to the default server port
"""


def get_config(path=DEFAULT_CONFIG_PATH):
    """Will return a :class:ConfigParser instance with the configuration
    loaded from a configuration file located under the given path. If
    the path does not exist a new initial configuration will be
    generated.

    :path: Path to the config file
    :returns: :class:ConfigParser instance

    """
    config = configparser.ConfigParser(allow_no_value=True,
                                       interpolation=configparser.ExtendedInterpolation())
    if not os.path.exists(path):
        with open(path, 'w') as configfile:
            config.read_string(DEFAULT_CONFIG)
            #  FIXME: Issue #1. Comments are lost when writing the
            #  configuration file. According to the documentation
            #  comments should be supported. (ti) <2017-04-19 23:07>
            config.write(configfile)
    else:
        config.read(path)
    return config
