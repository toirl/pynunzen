# -*- coding: utf-8 -*-

import click
import logging
from pynunzen.node.node import Node
from pynunzen.config import DEFAULT_CONFIG_PATH, get_config, get_node_server_address

LOGLEVEL = {
    "0": logging.ERROR,
    "1": logging.WARNING,
    "2": logging.INFO,
    "3": logging.DEBUG
}

log = logging.getLogger(__name__)


@click.group()
@click.option("--config",
              default=DEFAULT_CONFIG_PATH,
              help="Path to the configuration file.")
@click.option("-v", "--verbose", count=True,
              help="Set verbosity of the node.")
@click.pass_context
def main(ctx, config, verbose):
    """Console script for pynunzen client."""
    ctx.obj = {}
    ctx.obj["CONFIG"] = get_config(config)

    # Set verbosity depending on how often the user provides the "-v"
    # option.
    level = LOGLEVEL.get(str(verbose), logging.DEBUG)
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M')


@click.command()
@click.pass_context
def serve(ctx):
    """Will start the node server."""
    config = ctx.obj["CONFIG"]
    address = get_node_server_address(config)
    Node(address)


main.add_command(serve)
