from pvm.decoders.decoder import Decoder

class PcieTransactionLayerPacketHeaderRequestDecoder:
    def __init__(self, upstream_word_width):
        self._requester_id_decoder = Decoder(32, upstream_word_width, 16)
        self._tag_decoder = Decoder(48, upstream_word_width, 8)

    def decode(self, upstream_word_index, upstream_word):
        requester_id_valid, requester_id = self._requester_id_decoder.decode(upstream_word_index, upstream_word)
        tag_valid, tag = self._tag_decoder.decode(upstream_word_index, upstream_word)
        if requester_id_valid:
            requester_id = int.from_bytes(requester_id.to_bytes(2, 'big'), 'little')
        valid = (requester_id_valid and tag_valid)
        data = (requester_id, tag)
        error = 0
        return (valid, data, error)