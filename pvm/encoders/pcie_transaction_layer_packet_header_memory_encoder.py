from pvm.encoders.encoder import Encoder

class PcieTransactionLayerPacketHeaderMemoryEncoder:
    def __init__(self, downstream_word_width):
        self._address_msb_encoder = Encoder(64, downstream_word_width)
        self._address_lsb_encoder = Encoder(90, downstream_word_width)
        self._ph_encoder = Encoder(88, downstream_word_width)

    def encode(self, downstream_word_index, upstream_word):
        address, ph = upstream_word
        address_msb = (address >> 6)
        address_msb = int.from_bytes(address_msb.to_bytes(3, 'little'), 'big')
        address_lsb = address & 0x3F
        word = self._address_msb_encoder.encode(downstream_word_index, address_msb)
        word |= self._address_lsb_encoder.encode(downstream_word_index, address_lsb)
        word |= self._ph_encoder.encode(downstream_word_index, ph)
        return word