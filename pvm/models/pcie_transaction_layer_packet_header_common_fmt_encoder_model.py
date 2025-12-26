import cocotb

import pyuvm

from pvm.encoders.pcie_transaction_layer_packet_header_common_fmt_encoder import PcieTransactionLayerPacketHeaderCommonFmtEncoder

class PcieTransactionLayerPacketHeaderCommonFmtEncoderModel(pyuvm.uvm_subscriber):
    def build_phase(self):
        self._encoder = PcieTransactionLayerPacketHeaderCommonFmtEncoder(int(cocotb.top.DOWNSTREAM_WORD_WIDTH.value))
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    def write(self, indexed_word):
        word_index, tlp_prefix, data_indicator, header_length = indexed_word
        word_index, tlp_prefix, data_indicator, header_length = (int(word_index), int(tlp_prefix), int(data_indicator), int(header_length))
        word = self._encoder.encode(word_index, (tlp_prefix, data_indicator, header_length))
        self.analysis_port.write(word)