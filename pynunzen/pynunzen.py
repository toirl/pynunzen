# -*- coding: utf-8 -*-
import datetime
import hashlib
from pynunzen.helpers import utcts

__blockchain_version__ = "1.0"
"""Version of the blockchain. Used to versionize the blockchain."""
__block_version__ = "1.0"
"""Version of the block. Used to versionize the block."""


def validate_block(blockchain, block):
    """Will check if the given block is a valid block to be added to the
    block chain. Check is always done against the last block in the
    blockchain."""
    last_block = blockchain.end

    # Check if the given block links to the last block
    if last_block.address != block.parent:
        raise ValueError("Wrong hash for the previous block")

    # Check if the index is +1 to the index of the last block in the
    # blockchain.
    if last_block.index - block.index != -1:
        raise ValueError("Index of block does not match the index of the previos block")

    # Check if the address of the block is correct
    address = generate_block_address(block.index, block.timestamp, block.parent, block.data)
    if address != block.address:
        raise ValueError("Hash of block does not match calculated value.")

    return True


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
    index = 0
    timestamp = utcts(datetime.datetime(2017, 4, 7, 16, 3, 0))
    address = "f4a3ea59c413e6b470ed12757f3758ad70a4e9bff2954263f22be091871cb499"
    data = ["NY-Times on 7.04.2017: U.S. Strikes Syria Over Chemical Attack"]
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

    @property
    def length(self):
        """Will return the number of block which are contained in the blockchain"""
        return len(self.blocks)

    def append(self, block):
        """Will append the given block to the blockchain

        :block: :class:`Block` instance
        """
        validate_block(self, block)
        self.blocks.append(block)
