from pvm.encoders.pcie_transaction_layer_packet_header_common_encoder import PcieTransactionLayerPacketHeaderCommonEncoder
from pvm.encoders.pcie_transaction_layer_packet_header_request_encoder import PcieTransactionLayerPacketHeaderRequestEncoder

class PcieTransactionLayerPacketHeaderEncoder:
    def __init__(self, downstream_word_width):
        self._common_encoder = PcieTransactionLayerPacketHeaderCommonEncoder(downstream_word_width)
        self._request_encoder = PcieTransactionLayerPacketHeaderRequestEncoder(downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        common_fmt_tlp_prefix, common_fmt_data_indicator, common_fmt_header_length, common_packet_type, common_tc, common_attr_id_based_ordering, common_attr_relaxed_ordering, common_attr_no_snoop, common_th, common_td, common_ep, common_at, common_length, request_requester_id, request_tag = upstream_word
        word = self._common_encoder.encode(downstream_word_index, (common_fmt_tlp_prefix, common_fmt_data_indicator, common_fmt_header_length, common_packet_type, common_tc, common_attr_id_based_ordering, common_attr_relaxed_ordering, common_attr_no_snoop, common_th, common_td, common_ep, common_at, common_length))
        word |= self._request_encoder.encode(downstream_word_index, (request_requester_id, request_tag))
        return word