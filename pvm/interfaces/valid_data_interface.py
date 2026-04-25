import cocotb

from pvm.interfaces import DataInterface

class ValidDataInterface:
    def __init__(self, clk_pin, valid_pin, data_pin):
        self._valid_interface = DataInterface(clk_pin, valid_pin)
        self._data_interface = DataInterface(clk_pin, data_pin)

    async def put(self, sequence_item):
        await self.put_valid_data(sequence_item.valid, sequence_item.data)

    async def put_valid_data(self, valid, data):
        valid_interface_task = cocotb.start_soon(self._valid_interface.put_data(valid))
        data_interface_task = cocotb.start_soon(self._data_interface.put_data(data))
        await cocotb.triggers.Combine(valid_interface_task, data_interface_task)

    async def get(self):
        while True:
            data_interface_task = cocotb.start_soon(self._data_interface.get())
            valid = await self._valid_interface.get()
            if valid:
                return await data_interface_task