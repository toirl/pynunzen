# -*- coding: utf-8 -*-

import click


@click.group()
def main(args=None):
    """Console script for pynunzen client."""
    pass


@click.command()
def serve():
    """Will start the node server"""
    pass


main.add_command(serve)
