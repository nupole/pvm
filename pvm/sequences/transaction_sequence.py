import random

import pyuvm

class TransactionSequence(pyuvm.uvm_sequence):
    def __init__(self, name, is_transaction_list = [True], max_number_of_transactions = 10):
        super().__init__(name)
        self.set_is_transaction_list(is_transaction_list)
        self.set_max_number_of_transactions(max_number_of_transactions)

    def set_is_transaction_list(self, is_transaction_list):
        self._is_transaction_list = is_transaction_list

    def set_max_number_of_transactions(self, max_number_of_transactions):
        self._max_number_of_transactions = max_number_of_transactions

    async def body(self):
        number_of_transactions = 0
        while number_of_transactions < self._max_number_of_transactions:
            is_transaction = random.choice(self._is_transaction_list)
            sequence_item = self._get_next_sequence_item(is_transaction)
            await self.start_item(sequence_item)
            if is_transaction:
                number_of_transactions += 1
            await self.finish_item(sequence_item)
        sequence_item = self._get_next_sequence_item(False)
        await self.start_item(sequence_item)
        await self.finish_item(sequence_item)