#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

__block_version__ = "1.0"
"""Version of the block. Used to versionize the block."""


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


class Block(object):

    """Single block in a blockchain. A block is a container data
    structure that holds all transactions/data for inclusion in the
    blockchain.

    The block header consists a reference to a previous block hash,
    which links the block to block in the blockchain. Further there are
    some fields related to the mining like difficulty, timestamp, and
    nonce.  The last part is the merkle tree root which is used to
    summarize all transactions or data in the block.

    The header is followed by a long list of transactions/data."""

    def __init__(self, index, timestamp, parent, data, address=None):

        #
        # Block data/transactions
        #
        if not isinstance(data, list):
            raise ValueError("Data must be a list")
        self.data = data
        """Holds the data oft the block. Data must be a list."""

        #
        # Header data
        #
        self.version = __block_version__
        """Version of the block"""
        # Mining related fields
        self.timestamp = timestamp
        """UTC timestamp when was this block created."""
        self.difficulty = None
        self.nonce = None

        self.parent = parent
        """References the address of the previous Block in the
        blockchain."""
        #  TODO: Implement merkle tree. (ti) <2017-04-07 16:01>
        self.merkle_tree = None
        """Merkle tree to summarize all data in the block"""

        # Block identification. Please note that in reality the index
        # and address of the block is usually not stored in the block or
        # transmitted on the network. They get recalculated on each node
        # on the fly. However we will store those data in the block to
        # have them available.
        self.index = index
        """A simple index of the block also know as the `Block Height`"""
        if address is None:
            address = generate_block_address(index, self.timestamp, self.parent, data)
        self.address = address
        """Block header hash. A double hashed SHA256 build over fields
        of the header in the block"""
