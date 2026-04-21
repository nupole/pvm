import pyuvm

from pvm.sequences.transaction_sequence import TransactionSequence

class InstructionSequenceItem(pyuvm.uvm_sequence_item):
    def __init__(self, name, instruction):
        super().__init__(name)
        self.instruction = instruction

class InstructionIteratorSequence(TransactionSequence):
    def __init__(self, name, opcode_iterator, opcode_iterator_length):
        super().__init__(name, max_number_of_transactions = opcode_iterator_length - 1)
        self._opcode_iterator = opcode_iterator

    def _get_next_sequence_item(self, is_transaction):
        opcode = next(self._opcode_iterator)
        return InstructionSequenceItem('instruction_sequence', self._get_next_instruction(opcode))