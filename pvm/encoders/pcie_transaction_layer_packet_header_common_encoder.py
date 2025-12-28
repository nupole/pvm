from pvm.encoders.encoder import Encoder
from pvm.encoders.pcie_transaction_layer_packet_header_common_fmt_encoder import PcieTransactionLayerPacketHeaderCommonFmtEncoder
from pvm.encoders.pcie_transaction_layer_packet_header_common_attr_encoder import PcieTransactionLayerPacketHeaderCommonAttrEncoder

class PcieTransactionLayerPacketHeaderCommonEncoder:
    def __init__(self, downstream_word_width):
        self._fmt_encoder = PcieTransactionLayerPacketHeaderCommonFmtEncoder(downstream_word_width)
        self._packet_type_encoder = Encoder(0, downstream_word_width)
        self._tc_encoder = Encoder(12, downstream_word_width)
        self._attr_encoder = PcieTransactionLayerPacketHeaderCommonAttrEncoder(downstream_word_width)
        self._th_encoder = Encoder(8, downstream_word_width)
        self._td_encoder = Encoder(23, downstream_word_width)
        self._ep_encoder = Encoder(22, downstream_word_width)
        self._at_encoder = Encoder(18, downstream_word_width)
        self._length_msb_encoder = Encoder(16, downstream_word_width)
        self._length_lsb_encoder = Encoder(24, downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        fmt_tlp_prefix, fmt_data_indicator, fmt_header_length, packet_type, tc, attr_id_based_ordering, attr_relaxed_ordering, attr_no_snoop, th, td, ep, at, length = upstream_word
        length_msb = (length >> 8)
        length_lsb = length & 0xFF
        word = self._fmt_encoder.encode(downstream_word_index, (fmt_tlp_prefix, fmt_data_indicator, fmt_header_length))
        word |= self._packet_type_encoder.encode(downstream_word_index, packet_type)
        word |= self._tc_encoder.encode(downstream_word_index, tc)
        word |= self._attr_encoder.encode(downstream_word_index, (attr_id_based_ordering, attr_relaxed_ordering, attr_no_snoop))
        word |= self._th_encoder.encode(downstream_word_index, th)
        word |= self._td_encoder.encode(downstream_word_index, td)
        word |= self._ep_encoder.encode(downstream_word_index, ep)
        word |= self._at_encoder.encode(downstream_word_index, at)
        word |= self._length_msb_encoder.encode(downstream_word_index, length_msb)
        word |= self._length_lsb_encoder.encode(downstream_word_index, length_lsb)
        return word