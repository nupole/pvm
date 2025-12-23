import pyuvm

class Monitor(pyuvm.uvm_monitor):
    def __init__(self, name, parent, interface):
        super().__init__(name, parent)
        self._interface = interface

    def build_phase(self):
        self.analysis_port = pyuvm.uvm_analysis_port('analysis_port', self)

    async def run_phase(self):
        while True:
            data = await self._interface.get()
            self.analysis_port.write(data)