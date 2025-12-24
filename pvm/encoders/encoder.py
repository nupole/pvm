class Encoder:
    def __init__(self, downstream_word_bit_offset, downstream_word_width):
        self._WORD_INDEX = int(downstream_word_bit_offset / downstream_word_width)
        self._BIT_OFFSET = downstream_word_bit_offset % downstream_word_width

    def encode(self, word_index, word):
        downstream_word = 0
        if(word_index == self._WORD_INDEX):
            downstream_word = word << self._BIT_OFFSET
        return downstream_word