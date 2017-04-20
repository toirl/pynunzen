# -*- coding: utf-8 -*-

import click
from pynunzen.node.node import Node
from pynunzen.config import DEFAULT_CONFIG_PATH, get_config, get_node_server_address


@click.group()
@click.option("--config",
              default=DEFAULT_CONFIG_PATH,
              help="Path to the configuration file.")
@click.pass_context
def main(ctx, config):
    """Console script for pynunzen client."""
    ctx.obj = {}
    ctx.obj["CONFIG"] = get_config(config)


@click.command()
@click.pass_context
def serve(ctx):
    """Will start the node server."""
    config = ctx.obj["CONFIG"]
    address = get_node_server_address(config)
    Node(address)


main.add_command(serve)
