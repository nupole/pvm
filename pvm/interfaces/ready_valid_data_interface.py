import cocotb

from pvm.interfaces import DataInterface, ValidDataInterface
from pvm.sequences.data_sequence import DataSequenceItem
from pvm.sequences.valid_data_sequence import ValidDataSequenceItem

class ReadyValidDataInterface:
    def __init__(self, clk_pin, ready_pin, valid_pin, data_pin):
        self._ready_interface = DataInterface(clk_pin, ready_pin)
        self._valid_data_interface = ValidDataInterface(clk_pin, valid_pin, data_pin)

    async def put(self, sequence_item):
        if isinstance(sequence_item, DataSequenceItem):
            await self.put_ready(sequence_item.data)
        elif isinstance(sequence_item, ValidDataSequenceItem):
            await self.put_valid_data(sequence_item.valid, sequence_item.data)

    async def put_ready(self, ready):
        await self._ready_interface.put_data(ready)
        if ready:
            await self._is_consumed()

    async def put_valid_data(self, valid, data):
        await self._valid_data_interface.put_valid_data(valid, data)
        if valid:
            await self._is_consumed()

    async def get(self):
        return await self._is_consumed()

    async def _is_consumed(self):
        valid_data_interface_task = cocotb.start_soon(self._valid_data_interface.get())
        while not (await self._ready_interface.get()):
            pass
        return await valid_data_interface_task