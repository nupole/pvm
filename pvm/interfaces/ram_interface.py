import enum

import cocotb

from pvm.interfaces.data_interface import DataInterface

class RamInterface:
    class RamInterfaceType(enum.Enum):
        WRITE = enum.auto()
        READ = enum.auto()

    def __init__(self, interface_type, clk_pin, enable_pin, address_pin, data_pin):
        self._interface_type = interface_type
        self._enable_interface = DataInterface(clk_pin, enable_pin)
        self._address_interface = DataInterface(clk_pin, address_pin)
        self._data_interface = DataInterface(clk_pin, data_pin)

    async def put(self, sequence_item):
        await self.put_ram(sequence_item.enable, sequence_item.address, sequence_item.data)

    async def put_ram(self, enable, address, data):
        enable_interface_task = cocotb.start_soon(self._enable_interface.put_data(enable))
        address_interface_task = cocotb.start_soon(self._address_interface.put_data(address))
        if self._interface_type == RamInterface.RamInterfaceType.WRITE:
            data_interface_task = cocotb.start_soon(self._data_interface.put_data(data))
            await cocotb.triggers.Combine(enable_interface_task, address_interface_task, data_interface_task)
        else:
            await cocotb.triggers.Combine(enable_interface_task, address_interface_task)

    async def get(self):
        while True:
            address_interface_task = cocotb.start_soon(self._address_interface.get())
            data_interface_task = cocotb.start_soon(self._data_interface.get())
            if await self._enable_interface.get():
                address = await address_interface_task
                data = await data_interface_task
                return(address, data)