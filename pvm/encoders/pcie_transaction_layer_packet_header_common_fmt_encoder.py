from pvm.encoders.encoder import Encoder

class PcieTransactionLayerPacketHeaderCommonFmtEncoder:
    def __init__(self, downstream_word_width):
        self._tlp_prefix_encoder = Encoder(7, downstream_word_width)
        self._data_indicator_encoder = Encoder(6, downstream_word_width)
        self._header_length_encoder = Encoder(5, downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        tlp_prefix, data_indicator, header_length = upstream_word
        word = self._tlp_prefix_encoder.encode(downstream_word_index, tlp_prefix)
        word |= self._data_indicator_encoder.encode(downstream_word_index, data_indicator)
        word |= self._header_length_encoder.encode(downstream_word_index, header_length)
        return word