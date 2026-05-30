import cocotb

from pvm.protocols.pcie_transaction_layer_packet.pcie_transaction_layer_packet import PCIeTransactionLayerPacket
from pvm.encoders.pcie_transaction_layer_packet_header_request_encoder import PcieTransactionLayerPacketHeaderRequestEncoder

class PcieTransactionLayerPacketHeaderEncoder:
    def __init__(self, downstream_word_width):
        self.bytes_per_word = int(int(cocotb.top.DOWNSTREAM_WORD_WIDTH.value) / 8)
        self._request_encoder = PcieTransactionLayerPacketHeaderRequestEncoder(downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        common_fmt_tlp_prefix, common_fmt_data_indicator, common_fmt_header_length, common_packet_type, common_tc, common_attr_id_based_ordering, common_attr_relaxed_ordering, common_attr_no_snoop, common_th, common_td, common_ep, common_at, common_length, request_requester_id, request_tag = upstream_word
        packet = PCIeTransactionLayerPacket()
        packet.header.common.fmt_tlp_prefix = common_fmt_tlp_prefix
        packet.header.common.fmt_data_indicator = common_fmt_data_indicator
        packet.header.common.fmt_header_length = common_fmt_header_length
        packet.header.common.type = common_packet_type
        packet.header.common.tc = common_tc
        packet.header.common.attr_id_based_ordering = common_attr_id_based_ordering
        packet.header.common.attr_relaxed_ordering = common_attr_relaxed_ordering
        packet.header.common.attr_no_snoop = common_attr_no_snoop
        packet.header.common.th = common_th
        packet.header.common.td = common_td
        packet.header.common.ep = common_ep
        packet.header.common.at = common_at
        packet.header.common.length = common_length
        offset = self.bytes_per_word * downstream_word_index
        word = int.from_bytes(packet.get_bytes(offset, self.bytes_per_word))
        word |= self._request_encoder.encode(downstream_word_index, (request_requester_id, request_tag))
        return word