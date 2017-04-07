# -*- coding: utf-8 -*-
import datetime
import calendar
import hashlib

__blockchain_version__ = "1.0"
"""Version of the blockchain. Used to versionize the blockchain."""
__block_version__ = "1.0"
"""Version of the block. Used to versionize the block."""


def utcts(dt):
    """Will return a UTC timestamp of the given datetime"""
    if dt.tzinfo is not None:
        raise ValueError("Datetime must be naiv and must not contain any tzinfo")
    return calendar.timegm(dt.utctimetuple())


def generate_block_address(index, timestamp, parent, data):
    """Will calculate a doubled SHA256 hash which will be used as the
    address of a new created block in the blockchain.

    :index: index of the block
    :timestamp: timestamp of the block
    :parent: address of the previous block
    :data: data within the the block
    :returns: SHA256 hash

    """
    hash_source = str(index) + str(timestamp) + str(parent) + str(data)
    h1 = hashlib.sha256()
    h2 = hashlib.sha256()
    h1.update(hash_source.encode("utf-8"))
    h2.update(h1.hexdigest().encode("utf-8"))
    return h2.hexdigest()


def generate_genesis_block():
    """Will return a block instance for the very first block in the blockchain.

    :returns: :class:`Block`
    """
    index = 1
    timestamp = utcts(datetime.datetime(2017, 4, 5, 18, 0, 0))
    address = "235646d62fb74fd390c67795cc94d90f3fb94691f03a9265d573d12684ab98ec"
    data = "Hello Blockchain!"
    return Block(index, timestamp, None, data, address)


def generate_new_block(blockchain, data):
    """Will return a new block for the given blockchain. The block can
    than be added to the blockchain.

    :blockchain: :class:`Blockchain` instance
    :data: Payload of the Block
    :returns: class:`Block` instance

    """
    block = blockchain.end
    index = block.index + 1
    timestamp = utcts(datetime.datetime.utcnow())
    parent = block.address
    return Block(index, timestamp, parent, data)


class Block(object):

    """Single block in a blockchain. A block can store various
    informations within the data attribute. Each block is linked to its
    previous block. This links build up the blockchain."""

    def __init__(self, index, timestamp, parent, data, address=None):
        """TODO: to be defined1. """

        self.version = __block_version__
        """Version of the block"""
        self.index = index
        """A simple index of the block"""
        self.timestamp = timestamp
        """UTC timestamp"""
        if address is None:
            address = generate_block_address(index, timestamp, parent, data)
        self.address = address
        """SHA256 hash build over other fields of this block"""
        self.parent = parent
        """References the address of the previous Block in the blockchain."""
        self.data = data
        """Holds the data oft the block. Can be anything."""


class Blockchain(object):

    """Blockchain. Will hold a list of Blocks"""

    def __init__(self):
        self.blocks = [generate_genesis_block()]
        self.version = __blockchain_version__

    @property
    def end(self):
        """Will return the last block of the blockchain

        :returns: :class:`Block` instance

        """
        return self.blocks[-1]
