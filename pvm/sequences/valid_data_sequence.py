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

class RandomValidDataSequence(ValidDataSequence):
    def __init__(self, name, is_transaction_list = [True], max_number_of_transactions = 10, max_data = 15):
        super().__init__(name, is_transaction_list, max_number_of_transactions)
        self.set_max_data(max_data)

    def set_max_data(self, max_data):
        self._max_data = max_data

    def _get_data(self):
        return self._get_random_data()

    def _get_random_data(self):
        return random.randint(0, self._max_data)