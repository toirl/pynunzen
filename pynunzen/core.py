#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pynunzen.ledger.transaction import Transaction, Data, Coin


class Core(object):

    """Pynunzen Core. The core connects the different components and
    provides an interface to the client and server."""

    def __init__(self, blockchain, wallet):
        """
        The core takes two arguments. The is instantiated with a
        preloaded version of the `blockchain`.  As second argument the
        core takes a `wallet`.

        :blockchain: :class:Blockchain instance
        :wallet: :class:Wallet instance
        :returns: :class:Core instance
        """

        self.blockchain = blockchain
        """The distributed ledger called blockchain"""
        self.wallet = wallet
        """The wallet holds the private and public key and addresses."""
        self.global_utxo = {}
        """Dictionary with a list of *all* Unspent Transaction Outputs (UTXO)
        in the blockchain. An UTXO can be spent as an input in a new
        transaction."""
        self.utxo = {}
        """Dictionary with a list of Unspent Transaction Outputs (UTXO)
        in the blockchain which are emcumbered with one of one of the keys in
        the wallet. An UTXO can be spent as an input in a new
        transaction."""
        self.build_utxo()

    @property
    def balance(self):
        """Will return the balance of coins which are associated with
        this wallet."""
        total = 0
        for address in self.utxo:
            output = self.utxo[address]
            if isinstance(output, Coin):
                total += output.value
        return total

    def build_utxo(self):
        """Will build the list of UTXO. This is done by checking all
        transactions in the blockchain if the transaction contains
        data/value"""
        for block in self.blockchain.blocks:
            for transaction in block.data:
                for output in transaction.outputs:
                    address = output[0]
                    data = output[1]
                    if isinstance(data, Data):
                        self.global_utxo[address] = data
                        if address in self.wallet.addresses:
                            self.utxo[address] = data

    def get_transaction(self, data, address):
        """Will return a new :class:Transaction instance which will
        transfer the given `data` to the `address`

        :data: Data which will be transfered to the given address.
        :address: Address which will receive the data.
        :returns: :class:Transaction

        """
        if isinstance(data, Coin):
            # Check if we have enough coins
            if data.value > self.balance:
                raise ValueError("Not enough coins! You only have {} coins!".format(self.balance))
            else:
                # Although UTXO can be any arbitrary value, once created
                # it is indivisible just like a coin that cannot be cut
                # in half. If a UTXO is larger than the desired value of
                # a transaction, it must still be consumed in its
                # entirety and change must be generated in the
                # transaction. In other words, if you have a 20 bitcoin
                # UTXO and want to pay 1 bitcoin, your transaction must
                # consume the entire 20 bitcoin UTXO and produce two
                # outputs: one paying 1 bitcoin to your desired
                # recipient and another paying 19 bitcoin in change back
                # to your wallet. As a result, most bitcoin transactions
                # will generate change
                inputs = []
                total = 0
                for address in self.utxo:
                    total += self.utxo[address].value
                    inputs.append((address, self.utxo[address]))
                    change_address = address

                # Calculate difference between total and data.value to
                # create a new output for the change we will receive.
                change = total - data.value

                # Now create the outputs
                outputs = []
                if change:
                    outputs.append((change_address, Coin(change)))
                outputs.append((address, data))

                transaction = Transaction()
                transaction.outputs = outputs
                transaction.inputs = inputs

                return transaction

        raise ValueError("Can not build a transaction for data {} to {}".format(data, address))
