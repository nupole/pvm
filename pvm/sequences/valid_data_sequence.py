import random

import pyuvm

from pvm.sequences.transaction_sequence import TransactionSequence

class ValidDataSequenceItem(pyuvm.uvm_sequence_item):
    def __init__(self, name, valid, data):
        super().__init__(name)
        self.valid = valid
        self.data = data

class ValidDataSequence(TransactionSequence):
    def _get_next_sequence_item(self, is_transaction):
        if is_transaction:
            data = self._get_data()
        else:
            data = self._get_random_data()
        return ValidDataSequenceItem('valid_data_sequence_item', is_transaction, data)

