from pvm.decoders.pcie_transaction_layer_packet_header_common_decoder import PcieTransactionLayerPacketHeaderCommonDecoder
from pvm.decoders.pcie_transaction_layer_packet_header_request_decoder import PcieTransactionLayerPacketHeaderRequestDecoder

class PcieTransactionLayerPacketHeaderDecoder:
    def __init__(self, upstream_word_width):
        self._common_decoder = PcieTransactionLayerPacketHeaderCommonDecoder(upstream_word_width)
        self._request_decoder = PcieTransactionLayerPacketHeaderRequestDecoder(upstream_word_width)

    def decode(self, upstream_word_index, upstream_word):
        common_valid, common, common_error = self._common_decoder.decode(upstream_word_index, upstream_word)
        request_valid, request, request_error = self._request_decoder.decode(upstream_word_index, upstream_word)
        valid = (common_valid and request_valid)
        data = common + request
        error = common_error or request_error
        return (valid, data, error)