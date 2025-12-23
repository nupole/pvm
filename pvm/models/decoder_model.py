import cocotb

import pyuvm

from pvm.decoders.decoder import Decoder

class DecoderModel(pyuvm.uvm_subscriber):
    def build_phase(self):
        self._decoder = Decoder(int(cocotb.top.UPSTREAM_WORD_BIT_OFFSET.value), int(cocotb.top.UPSTREAM_WORD_WIDTH.value), int(cocotb.top.DOWNSTREAM_WORD_WIDTH.value))
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        word_index, word = indexed_word
        word_index, word = (int(word_index), int(word))
        word_valid, word = self._decoder.decode(word_index, word)
        if word_valid:
            self.analysis_port.write(word)