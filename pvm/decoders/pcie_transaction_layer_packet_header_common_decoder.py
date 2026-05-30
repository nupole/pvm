from pvm.protocols.pcie_transaction_layer_packet.pcie_transaction_layer_packet import PCIeTransactionLayerPacket
from pvm.decoders.decoder import Decoder
from pvm.decoders.pcie_transaction_layer_packet_header_common_attr_decoder import PcieTransactionLayerPacketHeaderCommonAttrDecoder

class PcieTransactionLayerPacketHeaderCommonDecoder:
    def __init__(self, upstream_word_width):
        self._packet = PCIeTransactionLayerPacket()
        self._packet_type_decoder = Decoder(0, upstream_word_width, 5)
        self._tc_decoder = Decoder(12, upstream_word_width, 3)
        self._attr_decoder = PcieTransactionLayerPacketHeaderCommonAttrDecoder(upstream_word_width)
        self._th_decoder = Decoder(8, upstream_word_width, 1)
        self._td_decoder = Decoder(23, upstream_word_width, 1)
        self._ep_decoder = Decoder(22, upstream_word_width, 1)
        self._at_decoder = Decoder(18, upstream_word_width, 2)
        self._length_msb_decoder = Decoder(16, upstream_word_width, 2)
        self._length_lsb_decoder = Decoder(24, upstream_word_width, 8)

    def decode(self, upstream_word_index, upstream_word):
        self._packet.copy_to(upstream_word_index * 2, upstream_word.to_bytes(2, 'big'))
        fmt_tlp_prefix = self._packet.header.common.fmt_tlp_prefix
        fmt_data_indicator = self._packet.header.common.fmt_data_indicator
        fmt_header_length = self._packet.header.common.fmt_header_length
        fmt_error = fmt_tlp_prefix and (fmt_data_indicator or fmt_header_length)
        packet_type_valid, packet_type = self._packet_type_decoder.decode(upstream_word_index, upstream_word)
        tc_valid, tc = self._tc_decoder.decode(upstream_word_index, upstream_word)
        attr_valid, attr, attr_error = self._attr_decoder.decode(upstream_word_index, upstream_word)
        th_valid, th = self._th_decoder.decode(upstream_word_index, upstream_word)
        td_valid, td = self._td_decoder.decode(upstream_word_index, upstream_word)
        ep_valid, ep = self._ep_decoder.decode(upstream_word_index, upstream_word)
        at_valid, at = self._at_decoder.decode(upstream_word_index, upstream_word)
        length_msb_valid, length_msb = self._length_msb_decoder.decode(upstream_word_index, upstream_word)
        length_lsb_valid, length_lsb = self._length_lsb_decoder.decode(upstream_word_index, upstream_word)
        length_valid = length_msb_valid and length_lsb_valid
        length = length_lsb
        if length_valid:
            length |= (length_msb << 8)
        valid = (packet_type_valid and tc_valid and attr_valid and th_valid and td_valid and ep_valid and at_valid and length_valid)
        data = (fmt_tlp_prefix, fmt_data_indicator, fmt_header_length, packet_type, tc) + attr + (th, td, ep, at, length)
        error = fmt_error or attr_error
        return (valid, data, error)