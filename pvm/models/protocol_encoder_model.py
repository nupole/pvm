import cocotb

import pyuvm

class ProtocolEncoderModel(pyuvm.uvm_subscriber):
    def __init__(self, name, parent, encoder):
        super().__init__(name, parent)
        self._encoder = encoder

    def build_phase(self):
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        indexed_word = tuple(int(x) for x in indexed_word)
        word_index, *word = indexed_word
        word = tuple(word)
        word = self._encoder.encode(word_index, word)
        self.analysis_port.write(word)