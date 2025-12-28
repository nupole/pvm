import cocotb

import pyuvm

from pvm.encoders.pcie_transaction_layer_packet_header_common_encoder import PcieTransactionLayerPacketHeaderCommonEncoder

class PcieTransactionLayerPacketHeaderCommonEncoderModel(pyuvm.uvm_subscriber):
    def build_phase(self):
        self._encoder = PcieTransactionLayerPacketHeaderCommonEncoder(int(cocotb.top.DOWNSTREAM_WORD_WIDTH.value))
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        indexed_word = tuple(int(x) for x in indexed_word)
        word_index, *word = indexed_word
        word = tuple(word)
        word = self._encoder.encode(word_index, word)
        self.analysis_port.write(word)