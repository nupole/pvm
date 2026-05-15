import enum

import cocotb

import pyuvm

class UArtModel(pyuvm.uvm_subscriber):
    class UArtModelState(enum.Enum):
        START_BIT = enum.auto()
        DATA_BITS = enum.auto()
        STOP_BIT = enum.auto()

    def build_phase(self):
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)
        clk_frequency = int(cocotb.top.CLK_FREQUENCY.value)
        baud_rate = int(cocotb.top.BAUD_RATE.value)
        self._frame_width = int(cocotb.top.FRAME_WIDTH.value)
        self._clks_per_baud_rate_beat = int(clk_frequency / baud_rate)
        self._baud_rate_beat_counter = 0
        self._data_r = 1
        self._frame_index = 0
        self._frame = 0
        self._state = UArtModel.UArtModelState.START_BIT

    def write(self, item):
        if self._baud_rate_beat_counter == (self._clks_per_baud_rate_beat - 1):
            data = int(item)
            match self._state:
                case UArtModel.UArtModelState.START_BIT:
                    if (not data) and self.data_r:
                        self._state = UArtModel.UArtModelState.DATA_BITS
                case UArtModel.UArtModelState.DATA_BITS:
                    self._frame = (data << (self._frame_width - 1)) | (self._frame >> 1)
                    if self._frame_index == (self._frame_width - 1):
                        self._state = UArtModel.UArtModelState.STOP_BIT
                    self._frame_index = (self._frame_index + 1) % self._frame_width
                case UArtModel.UArtModelState.STOP_BIT:
                    self._state = UArtModel.UArtModelState.START_BIT
                    if data:
                        self.analysis_port.write(self._frame)
            self.data_r = data
        self._baud_rate_beat_counter = (self._baud_rate_beat_counter + 1) % self._clks_per_baud_rate_beat