#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import datetime
from decimal import Decimal, getcontext
from pynunzen.helpers import double_sha256


__transaction_version__ = "1.0"
log = logging.getLogger(__name__)
getcontext().prec = 8


def generate_transaction_hash(transaction):
    """Will generate a hash based on the content of input and outputs of
    the given transaction. The hash is used as a address of the
    transaction within the blockchain.

    :transaction: :class:Transaction instance
    :returns: hash

    """
    value = str(transaction.time)
    value += str(transaction.version)
    for tx_in in transaction.inputs:
        value += str(tx_in.data.value)
        value += str(tx_in.script._script)
        value += str(tx_in.tx_hash)
        value += str(tx_in.utxo_idx)
    for tx_out in transaction.outputs:
        value += str(tx_out.data.value)
        value += str(tx_out.script._script)
    return double_sha256(value)


def validate_transaction(transaction, blockchain):
    """Will validate the given transaction. The transaction is validated against the following points:

       * The transaction’s syntax and data structure must be correct.
       * Neither lists of inputs or outputs are empty.
       * Transaction hash validate.
       * For each input, the referenced output must exist.

       TODO:

       * For each input, the referenced output cannot already be spent
         (is in  UTXO).
       * The transaction size in bytes is less than MAX_BLOCK_SIZE.
       * Each output value, as well as the total, must be within the
         allowed range of values (less than 21m coins, more than 0).
       * None of the inputs have hash=0, N=–1 (coinbase transactions
         should not be relayed).
       * nLockTime is less than or equal to INT_MAX.
       * The transaction size in bytes is greater than or equal to 100.
       * The number of signature operations contained in the transaction
         is less than the signature operation limit.
       * The unlocking script (scriptSig) can only push numbers on the
         stack, and the locking script (scriptPubkey) must match
         isStandard forms (this rejects "nonstandard" transactions).
       * A matching transaction in the pool, or in a block in the main
         branch, must exist.
       * For each input, if the referenced output exists in any other
         transaction in the pool, the transaction must be rejected.
       * For each input, look in the main branch and the transaction
         pool to find the referenced output transaction. If the output
         transaction is missing for any input, this will be an orphan
         transaction. Add to the orphan transactions pool, if a matching
         transaction is not already in the pool.
       * For each input, if the referenced output transaction is a
         coinbase output, it must have at least COINBASE_MATURITY (100)
         confirmations.
       * Using the referenced output transactions to get input values,
         check that each input value, as well as the sum, are in the
         allowed range of values (less than 21m coins, more than 0).
       * Reject if the sum of input values is less than sum of output values.
       * Reject if transaction fee would be too low to get into an empty block.
       * The unlocking scripts for each input must validate against the
         corresponding output locking scripts.

    :transaction: :class:Transaction object
    :returns: True or False

    """
    trans_checks = [_check_syntax, _check_io, _check_hash]
    for check in trans_checks:
        if check(transaction):
            continue
        else:
            log.error("Validation {} of transactoin failed".format(check.__name__))
            return False

    trans_block_checks = [_check_referenced_hash]
    for check in trans_block_checks:
        if check(transaction, blockchain):
            continue
        else:
            log.error("Validation {} of transactoin in context of the blockchain failed".format(check.__name__))
            return False
    log.debug("Validation of transaction successfull")
    return True


def _check_referenced_hash(transaction, blockchain):
    """Will check if the referenced outout in the transaction inputs are
    present in the blockchain and not already spent.

    :transaction: TODO
    :blockchain: TODO
    :returns: TODO

    """
    for tx_in in transaction.inputs:
        tx = blockchain.get_transaction(tx_in.tx_hash)
        if tx:
            # TODO: Implement check if outout is already spent. (ti) <2017-05-22 13:32>
            pass
        else:
            # Transaction not found.
            return False
    return True


def _check_hash(transaction):
    """The stored hash value of the transaction must be the same when rebuild from scratch

    :transaction: :class:Transaction
    :returns: True or False

    """
    tx_hash = transaction.hash
    return tx_hash == generate_transaction_hash(transaction)


def _check_syntax(transaction):
    """The transaction’s syntax and data structure must be correct.

    :transaction: :class:Transaction
    :returns: True or False

    """
    try:
        assert hasattr(transaction, "time")
        assert hasattr(transaction, "version")
        assert hasattr(transaction, "inputs")
        assert hasattr(transaction, "outputs")
        assert hasattr(transaction, "hash")
        assert len(transaction.__dict__) == 5
        return True
    except AssertionError:
        return False


def _check_io(transaction):
    """Neither lists of inputs or outputs are empty.

    :transaction: :class:Transaction
    :returns: True or False

    """
    return len(transaction.inputs) > 0 and len(transaction.outputs) > 0


class Data(object):

    """Container for the transfered data/value within a transaction."""

    def __init__(self, value):
        self.value = value

    def check(self, value):
        """Will return True if the current container includes the given
        value.

        :value: Value to be checked
        :returns: True or False

        """
        raise NotImplementedError()


class Coin(Data):

    def __init__(self, value):
        value = Decimal(value)
        super(Coin, self).__init__(value)

    def check(self, value):
        try:
            value = Decimal(value)
        except:
            raise ValueError("'{}' can not be casted to Decimal".format(value))
        return self.value > 0


class LockScript(object):

    """A locking script is an encumbrance placed on an output, and it
    specifies the conditions that must be met to spend the output in the
    future. Most of the time this is the public address of the receiver
    of the transaction."""

    def __init__(self, script):
        self._script = script

    def unlock(self, script):
        return self._script == script


class UnlockScript(object):

    """An unlocking script is a script that "solves," or satisfies, the
    conditions placed on an output by a locking script and allows the
    output to be spent. Unlocking scripts are part of every transaction
    input, and most of the time they contain a digital signature
    produced by the user’s wallet from his or her private key"""

    def __init__(self, script):
        self._script = script


class Output(object):

    """Output for a transaction. Transaction outputs consist of two
    parts: An amount of data which is about to be transferred, and a
    locking script, also known as an "encumbrance" that "locks" this
    data by specifying the conditions that must be met to spend the
    output"""

    def __init__(self, data, script):
        """

        :data: :class:Data instance.
        :script: :class:LockScript instance.

        """
        self.data = data
        self.script = script


class Input(object):

    """In simple terms, transaction inputs are pointers to UTXO. They
    point to a specific UTXO by reference to the transaction hash and
    sequence number where the UTXO is recorded in the blockchain. To
    spend UTXO, a transaction input also includes unlocking scripts that
    satisfy the spending conditions set by the UTXO. The unlocking
    script is usually a signature proving ownership of the bitcoin
    address that is in the locking script."""

    def __init__(self, data, script, tx_hash, utxo_idx):
        """

        :data: :class:Data instance.
        :script: :class:UnlockScript instance.
        :txhash: Reference to the hash of the transaction with unspent
        outputs.
        :utxo_idx: Index to the unspent output in the referenced
        transaction (txhash). 0 is the first.

        """
        self.data = data
        self.script = script
        self.tx_hash = tx_hash
        self.utxo_idx = utxo_idx


class CoinbaseInput(Input):

    """The coinbase input is a special input. It is the input of the
    first transaction within a new block. It is the origin of the reward
    for the miner who generated the new block. As this input has no
    reference to a origin output it has some special logic to unlock
    the input."""

    def __init__(self, data, script, coinbase_script):
        tx_hash = "0" * 32
        utxo_idx = 0
        Input.__init__(self, data, script, tx_hash, utxo_idx)
        self.coinbase_script = coinbase_script


class Transaction(object):

    """A transaction is a data structure that encodes a transfer of
    value from a source of data/value, called an input, to a destination,
    called an output."""

    def __init__(self, inputs, outputs):
        """TODO: to be defined1. """
        self.version = __transaction_version__
        """Version of this transaction"""
        self.time = str(datetime.datetime.utcnow())
        """Time when the the transaction was created"""
        self.inputs = inputs
        """One or more transaction inputs"""
        self.outputs = outputs
        """One or more transaction outputs"""
        self.hash = generate_transaction_hash(self)
        """Hash of this transaction, A hash is some kind of a address of
        the transaction within the blockchain. It is used to link
        outouts from inputs in other transactions."""
