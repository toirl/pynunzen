#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ledger
----------------------------------

Tests for `ledger` package.
"""

import pytest
import datetime

from pynunzen.helpers import utcts
from pynunzen.ledger.blockchain import (
    Blockchain,
    validate_block,
    generate_genesis_block,
    generate_new_block,
    GENESIS_BLOCK_INPUT,
    GENESIS_BLOCK_ADDRESS
)
from pynunzen.ledger.block import generate_block_address, __block_max_size__
from pynunzen.ledger.transaction import Transaction, Coin, Output, LockScript, Input, UnlockScript, Data, CoinbaseInput
from .test_wallet import alice_wallet, bob_wallet

@pytest.fixture
def blockchain(alice_wallet, bob_wallet):
    blockchain = Blockchain()

    # 1. Generate a coinbasetransaction for for the first block. Add
    # 1000 coins for alice.
    for x in range(4):
        cb_tx_in = CoinbaseInput(Data("xxx"), UnlockScript(None), UnlockScript(None))
        cb_tx_out = Output(Coin(1000), LockScript(list(alice_wallet.addresses)[0]))
        alice_cb_tx = Transaction([cb_tx_in], [cb_tx_out])
        blockchain.append(generate_new_block(blockchain, [alice_cb_tx]))

    # 2. Generate a coinbasetransaction for for the seconds block. Add
    # 1000 coins for bob.
    for x in range(6):
        cb_tx_in = CoinbaseInput(Data("xxx"), UnlockScript(None), UnlockScript(None))
        cb_tx_out = Output(Coin(1000), LockScript(list(bob_wallet.addresses)[0]))
        bob_cb_tx = Transaction([cb_tx_in], [cb_tx_out])
        blockchain.append(generate_new_block(blockchain, [bob_cb_tx]))
    return blockchain


@pytest.fixture
def transaction():
    """Fixture for a empty blockchain."""
    tx_input = Input(Data(""), UnlockScript(None), "dummytxhash", 0)
    tx_output = Output(Data(""), LockScript(None))
    return Transaction([tx_input], [tx_output])

@pytest.fixture
def coinbasetransaction():
    """Fixture for a empty blockchain."""
    tx_input = CoinbaseInput(Data("random"), LockScript(None), LockScript(None))
    tx_output = Output(Coin(50), LockScript("dummyaddress"))
    return Transaction([tx_input], [tx_output])


@pytest.fixture
def blockchain_modified_genesis(blockchain):
    """Fixture for a empty blockchain. And a modified genesis Block."""
    genesis_block = blockchain.blocks[0]
    genesis_block.address = "hashismodified"
    blockchain.blocks[0] = genesis_block
    return blockchain


@pytest.fixture
def block_with_modified_genesis(blockchain_modified_genesis, coinbasetransaction, transaction):
    """Fixture for a empty block."""
    return generate_new_block(blockchain_modified_genesis, [coinbasetransaction, transaction, transaction])


@pytest.fixture
def block(blockchain, coinbasetransaction, transaction):
    """Fixture for a empty block."""
    return generate_new_block(blockchain, [coinbasetransaction, transaction, transaction])


def test_generate_block_address():
    dt = datetime.datetime(2017, 1, 1, 12, 0, 0)
    index = 1
    timestamp = utcts(dt)
    parent = "parent"
    data = ["My data"]
    address = generate_block_address(index, timestamp, parent, data)
    assert address == "27edb13573987de43e061a400f89bbb10992b3b88c5356deaad2344ae2e77c6b"


def test_generate_genesis_block():
    block = generate_genesis_block()
    assert block.index == 0
    assert block.address == GENESIS_BLOCK_ADDRESS
    assert block.data[0].inputs[0].data.value == GENESIS_BLOCK_INPUT


def test_generate_new_block(blockchain, block, coinbasetransaction, transaction):
    assert block.index == 11
    assert block.parent == blockchain.end.address
    assert block.data == [coinbasetransaction, transaction, transaction]


def test_generate_new_block_non_coinbase_fail(blockchain, transaction):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, [transaction, transaction])


def test_generate_new_block_fail_length_output_coinbase(blockchain, coinbasetransaction, transaction):
    with pytest.raises(ValueError):
        coinbasetransaction.outputs = []
        generate_new_block(blockchain, [coinbasetransaction, transaction])


def test_generate_new_block_fail_length_input_coinbase(blockchain, coinbasetransaction, transaction):
    with pytest.raises(ValueError):
        coinbasetransaction.inputs = []
        generate_new_block(blockchain, [coinbasetransaction, transaction])


def test_block_validation_ok(blockchain, block):
    result = validate_block(blockchain, block)
    assert result is True


def test_block_validation_modified_genesis(blockchain_modified_genesis,
                                           block_with_modified_genesis):
    with pytest.raises(ValueError):
        validate_block(blockchain_modified_genesis, block_with_modified_genesis)


def test_block_validation_fails_index(blockchain, block):
    block.index = 23
    with pytest.raises(ValueError):
        validate_block(blockchain, block)


def test_block_validation_fails_parent(blockchain, block):
    block.parent += "a"
    with pytest.raises(ValueError):
        validate_block(blockchain, block)


def test_block_validation_fails_address(blockchain, block):
    block.address += "a"
    with pytest.raises(ValueError):
        validate_block(blockchain, block)


def test_add_block(blockchain, block):
    blockchain.append(block)
    assert blockchain.length == 12


def test_add_block_fail(blockchain, block, coinbasetransaction, transaction):
    fail_block = generate_new_block(blockchain, [coinbasetransaction, transaction])
    blockchain.append(block)
    with pytest.raises(ValueError):
        blockchain.append(fail_block)


def test_wrong_block_data_container(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, "Foo")


def test_wrong_block_data_type(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, ["Foo"])


def test_max_size_block_data(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, [x for x in range(__block_max_size__ + 1)])


def test_min_size_block_data(blockchain):
    with pytest.raises(ValueError):
        generate_new_block(blockchain, [])


def test_get_transaction(blockchain):
    tx_hash = blockchain.blocks[4].data[0].hash
    tx = blockchain.get_transaction(tx_hash)
    assert tx.outputs[0].script._script == "15PFxDy7xiw4dQxCnar1pdJUbN7MB1Wigr"
    assert tx.outputs[0].data.value == 1000


def test_get_transaction_fail(blockchain):
    tx = blockchain.get_transaction("xxx")
    assert tx is None
