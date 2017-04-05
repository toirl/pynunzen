# -*- coding: utf-8 -*-
import calendar
import hashlib


def utcts(dt):
    """Will return a UTC timestamp of the given datetime"""
    if dt.tzinfo is not None:
        raise ValueError("Datetime must be naiv and must not contain any tzinfo")
    return calendar.timegm(dt.utctimetuple())


def generate_block_address(index, timestamp, parent, data):
    """Will calculate a SHA256 hash which will be used as the address of
    a new created block in the blockchain.

    :index: index of the block
    :timestamp: timestamp of the block
    :parent: address of the previous block
    :data: data within the the block
    :returns: SHA256 hash

    """
    address = hashlib.sha256()
    address.update(bytes(index) + bytes(timestamp) + bytes(parent.encode("utf8")) + bytes(str(data).encode("utf8")))
    return address.hexdigest()


class Block(object):

    """Single block in a blockchain. A block can store various
    informations within the data attribute. Each block is linked to its
    previous block. This links build up the blockchain."""

    def __init__(self, index, timestamp, parent, data):
        """TODO: to be defined1. """

        self.index = index
        """A simple index of the block"""
        self.timestamp = timestamp
        """UTC timestamp"""
        self.address = generate_block_address(index, timestamp, parent, data)
        """SHA256 hash build over other fields of this block"""
        self.parent = None
        """References the address of the previous Block in the blockchain."""
        self.data = None
        """Holds the data oft the block. Can be anything."""
