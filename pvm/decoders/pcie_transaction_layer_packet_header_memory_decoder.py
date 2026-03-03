from pvm.decoders.decoder import Decoder

class PcieTransactionLayerPacketHeaderMemoryDecoder:
    def __init__(self, upstream_word_width):
        self._address_msb_decoder = Decoder(64, upstream_word_width, 24)
        self._address_lsb_decoder = Decoder(90, upstream_word_width, 6)
        self._ph_decoder = Decoder(88, upstream_word_width, 2)

    def decode(self, upstream_word_index, upstream_word):
        address_msb_valid, address_msb = self._address_msb_decoder.decode(upstream_word_index, upstream_word)
        address_lsb_valid, address_lsb = self._address_lsb_decoder.decode(upstream_word_index, upstream_word)
        ph_valid, ph = self._ph_decoder.decode(upstream_word_index, upstream_word)
        address_valid = address_msb_valid and address_lsb_valid
        address = address_lsb
        if address_valid:
            address |= (int.from_bytes(address_msb.to_bytes(3, 'big'), 'little') << 6)
        valid = (address_valid and ph_valid)
        data = (address, ph)
        error = 0
        return  (valid, data, error)