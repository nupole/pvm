from pvm.sequences.transaction_sequence import TransactionSequence
from pvm.sequences.data_sequence import DataSequenceItem

class ReadySequence(TransactionSequence):
    def _get_next_sequence_item(self, is_transaction):
        return DataSequenceItem('ready_sequence_item', is_transaction)