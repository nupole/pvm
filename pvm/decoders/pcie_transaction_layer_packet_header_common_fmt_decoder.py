from pvm.decoders.decoder import Decoder

class PcieTransactionLayerPacketHeaderCommonFmtDecoder:
    def __init__(self, upstream_word_width):
        self._tlp_prefix_decoder = Decoder(7, upstream_word_width, 1)
        self._data_indicator_decoder = Decoder(6, upstream_word_width, 1)
        self._header_length_decoder = Decoder(5, upstream_word_width, 1)

    def decode(self, upstream_word_index, upstream_word):
        tlp_prefix_valid, tlp_prefix = self._tlp_prefix_decoder.decode(upstream_word_index, upstream_word)
        data_indicator_valid, data_indicator = self._data_indicator_decoder.decode(upstream_word_index, upstream_word)
        header_length_valid, header_length = self._header_length_decoder.decode(upstream_word_index, upstream_word)
        valid = (tlp_prefix_valid and data_indicator_valid and header_length_valid)
        error = tlp_prefix and (data_indicator or header_length)
        return (valid, (tlp_prefix, data_indicator, header_length), error)