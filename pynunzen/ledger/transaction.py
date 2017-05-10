#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


__transaction_version__ = "1.0"
log = logging.getLogger(__name__)


def validate_transaction(transaction):
    """Will validate the given transaction. The transaction is validated against the following points:

       * The transaction’s syntax and data structure must be correct.
       * Neither lists of inputs or outputs are empty.

       TODO:

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
       * For each input, the referenced output must exist and cannot
         already be spent.
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
    checks = [_check_syntax, _check_io]
    for check in checks:
        if check(transaction):
            continue
        else:
            log.error("Validation {} of transactoin failed".format(check.__name__))
            return False
    else:
        log.debug("Validation of transaction successfull")
    return True


def _check_syntax(transaction):
    """The transaction’s syntax and data structure must be correct.

    :transaction: :class:Transaction
    :returns: True or False

    """
    try:
        assert hasattr(transaction, "version")
        assert hasattr(transaction, "inputs")
        assert hasattr(transaction, "outputs")
        assert len(transaction.__dict__) == 3
        return True
    except AssertionError:
        return False


def _check_io(transaction):
    """Neither lists of inputs or outputs are empty.

    :transaction: :class:Transaction
    :returns: True or False

    """
    return len(transaction.inputs) > 0 and len(transaction.outputs) > 0


class Transaction(object):

    """A transaction is a data structure that encodes a transfer of
    value from a source of data/value, called an input, to a destination,
    called an output."""

    def __init__(self):
        """TODO: to be defined1. """
        self.version = __transaction_version__
        """Version of this transaction"""
        self.inputs = []
        """One or more transaction inputs"""
        self.outputs = []
        """One or more transaction outputs"""
