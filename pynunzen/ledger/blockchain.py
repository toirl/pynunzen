#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from pynunzen.helpers import utcts
from pynunzen.ledger.block import Block, generate_block_address
from pynunzen.ledger.transaction import Transaction, Input, Data, UnlockScript

__blockchain_version__ = "1.0"
"""Version of the blockchain. Used to versionize the blockchain."""

GENESIS_BLOCK_ADDRESS = "f4a3ea59c413e6b470ed12757f3758ad70a4e9bff2954263f22be091871cb499"
GENESIS_BLOCK_INPUT = "NY-Times on 7.04.2017: U.S. Strikes Syria Over Chemical Attack"


def generate_genesis_block():
    """Will return a block instance for the very first block in the blockchain.

    :returns: :class:`Block`
    """
    index = 0

    # Build empty pseudo input.
    tx_in = Input(Data("NY-Times on 7.04.2017: U.S. Strikes Syria Over Chemical Attack"),
                  UnlockScript(None), tx_hash="" * 32, utxo_idx=0)
    transaction = Transaction([tx_in], [])
    data = [transaction]

    timestamp = utcts(datetime.datetime(2017, 4, 7, 16, 3, 0))
    address = GENESIS_BLOCK_ADDRESS
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

    if blockchain.blocks[0].address != GENESIS_BLOCK_ADDRESS:
        raise ValueError("Blockchain does not start with know genesis block")

    # Check if the address of the block is correct
    address = generate_block_address(block.index, block.timestamp, block.parent, block.data)
    if address != block.address:
        raise ValueError("Hash of block does not match calculated value.")

    return True


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
