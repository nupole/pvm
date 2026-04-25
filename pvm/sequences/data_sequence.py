import random

import pyuvm

from pvm.sequences.transaction_sequence import TransactionSequence

class DataSequenceItem(pyuvm.uvm_sequence_item):
    def __init__(self, name, data):
        super().__init__(name)
        self.data = data

class IterableDataSequence(TransactionSequence):
    def __init__(self, name, iterable = []):
        super().__init__(name, max_number_of_transactions = len(iterable) - 1)
        self._iterator = iter(iterable)

    def _get_next_sequence_item(self, is_transaction):
        data = next(self._iterator)
        return DataSequenceItem('iterable_data_sequence_item', data)

class IndexedRandomWordSequence(TransactionSequence):
    def __init__(self, name, is_word_list = [True], max_number_of_words = 64, max_word_index = 16, max_word = 15):
        super().__init__(name, is_word_list, max_number_of_words)
        self._max_word_index = max_word_index
        self._max_word = max_word
        self._word_index = 0

    def _get_next_sequence_item(self, is_transaction):
        word_index = self._word_index
        if is_transaction:
            self._word_index += 1
            self._word_index %= self._max_word_index
        word = random.randint(0, self._max_word)
        return DataSequenceItem('indexed_random_word_sequence_item', (word_index, word))