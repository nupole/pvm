from pvm.encoders.encoder import Encoder

class PcieTransactionLayerPacketHeaderRequestEncoder:
    def __init__(self, downstream_word_width):
        self._requester_id_encoder = Encoder(32, downstream_word_width)
        self._tag_encoder = Encoder(48, downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        requester_id, tag = upstream_word
        requester_id = int.from_bytes(requester_id.to_bytes(2, 'little'), 'big')
        word = self._requester_id_encoder.encode(downstream_word_index, requester_id)
        word |= self._tag_encoder.encode(downstream_word_index, tag)
        return word