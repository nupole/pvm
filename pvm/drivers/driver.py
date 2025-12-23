import pyuvm

class Driver(pyuvm.uvm_driver):
    def __init__(self, name, parent, interface):
        super().__init__(name, parent)
        self._interface = interface

    async def run_phase(self):
        while True:
            sequence_item = await self.seq_item_port.get_next_item()
            await self._interface.put(sequence_item)
            self.seq_item_port.item_done()