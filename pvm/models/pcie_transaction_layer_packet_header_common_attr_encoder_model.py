import cocotb

import pyuvm

from pvm.encoders.pcie_transaction_layer_packet_header_common_attr_encoder import PcieTransactionLayerPacketHeaderCommonAttrEncoder

class PcieTransactionLayerPacketHeaderCommonAttrEncoderModel(pyuvm.uvm_subscriber):
    def build_phase(self):
        self._encoder = PcieTransactionLayerPacketHeaderCommonAttrEncoder(int(cocotb.top.DOWNSTREAM_WORD_WIDTH.value))
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        word_index, id_based_ordering, relaxed_ordering, no_snoop = indexed_word
        word_index, id_based_ordering, relaxed_ordering, no_snoop = (int(word_index), int(id_based_ordering), int(relaxed_ordering), int(no_snoop))
        word = self._encoder.encode(word_index, (id_based_ordering, relaxed_ordering, no_snoop))
        self.analysis_port.write(word)