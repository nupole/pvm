import cocotb

import pyuvm

from pvm.sequences.ready_sequence import ReadySequence
from pvm.sequences.valid_data_sequence import ValidDataSequence

class ReadyValidDataSequence(pyuvm.uvm_sequence):
    def __init__(self, name):
        super().__init__(name)
        max_number_of_ready_transactions = pyuvm.ConfigDB().get(None, '', 'MAX_NUMBER_OF_READY_TRANSACTIONS')
        self._ready_sequence = ReadySequence.create('ready_sequence')
        self._ready_sequence.set_max_number_of_transactions(max_number_of_ready_transactions)
        max_number_of_valid_data_transactions = pyuvm.ConfigDB().get(None, '', 'MAX_NUMBER_OF_VALID_DATA_TRANSACTIONS')
        self._valid_data_sequence = ValidDataSequence.create('valid_data_sequence')
        self._valid_data_sequence.set_max_number_of_transactions(max_number_of_valid_data_transactions)

    async def body(self):
        ready_sequencer = pyuvm.ConfigDB().get(None, '', 'READY_SEQUENCER')
        valid_data_sequencer = pyuvm.ConfigDB().get(None, '', 'VALID_DATA_SEQUENCER')
        await cocotb.triggers.Combine(cocotb.start_soon(self._ready_sequence.start(ready_sequencer)),
                                      cocotb.start_soon(self._valid_data_sequence.start(valid_data_sequencer)))

class FastTransmitterSlowReceiverSequence(ReadyValidDataSequence):
    def __init__(self, name):
        super().__init__(name)
        self._ready_sequence.set_is_transaction_list([False, False, False, False, False, False, False, True])

class SlowTransmitterFastReceiverSequence(ReadyValidDataSequence):
    def __init__(self, name):
        super().__init__(name)
        self._valid_data_sequence.set_is_transaction_list([False, False, False, False, False, False, False, True])

class TransmitterReceiverSequence(pyuvm.uvm_sequence):
    async def body(self):
        fast_transmitter_slow_receiver_sequence = FastTransmitterSlowReceiverSequence('fast_transmitter_slow_receiver_sequence')
        slow_transmitter_fast_receiver_sequence = SlowTransmitterFastReceiverSequence('slow_transmitter_fast_receiver_sequence')
        await fast_transmitter_slow_receiver_sequence.start()
        await slow_transmitter_fast_receiver_sequence.start()