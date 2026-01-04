import cocotb

import pyuvm

from pvm.decoders.pcie_transaction_layer_packet_header_request_decoder import PcieTransactionLayerPacketHeaderRequestDecoder

class PcieTransactionLayerPacketHeaderRequestDecoderModel(pyuvm.uvm_subscriber):
    def build_phase(self):
        self._decoder = PcieTransactionLayerPacketHeaderRequestDecoder(int(cocotb.top.UPSTREAM_WORD_WIDTH.value))
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        word_index, word = indexed_word
        word_index, word = (int(word_index), int(word))
        word_valid, word, word_error = self._decoder.decode(word_index, word)
        if word_valid:
            self.analysis_port.write(word + (word_error,))