import random

import pyuvm

from pvm.sequences.transaction_sequence import TransactionSequence

class RamSequenceItem(pyuvm.uvm_sequence_item):
    def __init__(self, name, enable, address, data):
        super().__init__(name)
        self.enable = enable
        self.address = address
        self.data = data

class RamSequence(TransactionSequence):
    def __init__(self, name, valid_list = [True], max_number_of_transactions = 10, max_address = 15, max_data = 15):
        super().__init__(name, valid_list, max_number_of_transactions)
        self._max_address = max_address
        self._max_data = max_data

    def _get_next_sequence_item(self, is_transaction):
        if is_transaction:
            address, data = self._get_next_ram_data()
        else:
            address = random.randint(0, self._max_address)
            data = random.randint(0, self._max_data)
        return RamSequenceItem('ram_sequence_item', is_transaction, address, data)

class RandomRamSequence(RamSequence):
    def _get_next_ram_data(self):
        address = random.randint(0, self._max_address)
        data = random.randint(0, self._max_data)
        return (address, data)

class IncrementingAddressRamSequence(RamSequence):
    def __init__(self, name, valid_list = [True], max_address = 15, max_data = 15):
        super().__init__(name, valid_list, max_address + 1, max_address, max_data)
        self._address = 0

    def _get_next_ram_data(self):
        address = self._current_address
        data = random.randint(0, self._max_data)
        self._current_address += 1
        return (address, data)