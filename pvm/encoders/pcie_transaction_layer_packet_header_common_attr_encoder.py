from pvm.encoders.encoder import Encoder

class PcieTransactionLayerPacketHeaderCommonAttrEncoder:
    def __init__(self, downstream_word_width):
        self._id_based_ordering_encoder = Encoder(10, downstream_word_width)
        self._relaxed_ordering_encoder = Encoder(21, downstream_word_width)
        self._no_snoop_encoder = Encoder(20, downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        id_based_ordering, relaxed_ordering, no_snoop = upstream_word
        word = self._id_based_ordering_encoder.encode(downstream_word_index, id_based_ordering)
        word |= self._relaxed_ordering_encoder.encode(downstream_word_index, relaxed_ordering)
        word |= self._no_snoop_encoder.encode(downstream_word_index, no_snoop)
        return word