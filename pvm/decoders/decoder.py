class Decoder:
    def __init__(self, upstream_word_bit_offset, upstream_word_width, downstream_word_width):
        self._WORD_INDEX = int(upstream_word_bit_offset / upstream_word_width)
        self._BIT_OFFSET = upstream_word_bit_offset % upstream_word_width
        self._WORD_MASK = (2 ** downstream_word_width) - 1
        self._word_valid = False
        self._word = None

    def decode(self, word_index, word):
        if(word_index == self._WORD_INDEX):
            self._word_valid = True
            self._word = (word >> self._BIT_OFFSET) & self._WORD_MASK
        return (self._word_valid, self._word)