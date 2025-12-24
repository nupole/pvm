import cocotb

import pyuvm

from pvm.encoders.encoder import Encoder

class EncoderModel(pyuvm.uvm_subscriber):
    def build_phase(self):
        self._encoder = Encoder(int(cocotb.top.DOWNSTREAM_WORD_BIT_OFFSET.value), int(cocotb.top.DOWNSTREAM_WORD_WIDTH.value))
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        word_index, word = indexed_word
        word_index, word = (int(word_index), int(word))
        word = self._encoder.encode(word_index, word)
        self.analysis_port.write(word)