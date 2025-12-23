import cocotb

class DataInterface:
    def __init__(self, clk_pin, data_pin):
        self._clk_pin = clk_pin
        self._data_pin = data_pin

    async def put(self, sequence_item):
        await self.put_data(sequence_item.data)

    async def put_data(self, data):
        await cocotb.triggers.RisingEdge(self._clk_pin)
        if isinstance(self._data_pin, tuple):
            for i, data_pin in zip(data, self._data_pin):
                data_pin.value = i
        else:
            self._data_pin.value = data

    async def get(self):
        while True:
            await cocotb.triggers.FallingEdge(self._clk_pin)
            if isinstance(self._data_pin, tuple):
                data = []
                is_resolvable = True
                for data_pin in self._data_pin:
                    is_resolvable = is_resolvable and data_pin.value.is_resolvable
                    data.append(data_pin.value)
                if is_resolvable:
                    return tuple(data)
            else:
                if self._data_pin.value.is_resolvable:
                    return self._data_pin.value