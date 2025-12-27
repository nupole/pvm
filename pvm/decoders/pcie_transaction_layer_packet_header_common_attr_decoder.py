from pvm.decoders.decoder import Decoder

class PcieTransactionLayerPacketHeaderCommonAttrDecoder:
    def __init__(self, upstream_word_width):
        self._id_based_ordering_decoder = Decoder(10, upstream_word_width, 1)
        self._relaxed_ordering_decoder = Decoder(21, upstream_word_width, 1)
        self._no_snoop_decoder = Decoder(20, upstream_word_width, 1)

    def decode(self, upstream_word_index, upstream_word):
        id_based_ordering_valid, id_based_ordering = self._id_based_ordering_decoder.decode(upstream_word_index, upstream_word)
        relaxed_ordering_valid, relaxed_ordering = self._relaxed_ordering_decoder.decode(upstream_word_index, upstream_word)
        no_snoop_valid, no_snoop = self._no_snoop_decoder.decode(upstream_word_index, upstream_word)
        valid = (id_based_ordering_valid and relaxed_ordering_valid and no_snoop_valid)
        error = 0
        return (valid, (id_based_ordering, relaxed_ordering, no_snoop), error)