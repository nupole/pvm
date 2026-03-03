import cocotb

import pyuvm

class ProtocolDecoderModel(pyuvm.uvm_subscriber):
    def __init__(self, name, parent, decoder):
        super().__init__(name, parent)
        self._decoder = decoder

    def build_phase(self):
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        word_index, word = indexed_word
        word_index, word = (int(word_index), int(word))
        word_valid, word, word_error = self._decoder.decode(word_index, word)
        if word_valid:
            self.analysis_port.write(word + (word_error,))