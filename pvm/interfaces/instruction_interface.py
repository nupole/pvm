import cocotb

from pvm.interfaces import DataInterface

class InstructionInterface:
    def __init__(self, clk_pin, opcode_pin, operand_pin):
        self._opcode_interface = DataInterface(clk_pin, opcode_pin)
        self._operand_interface = DataInterface(clk_pin, operand_pin)

    async def put(self, sequence_item):
        await self.put_instruction(sequence_item.instruction)

    async def put_instruction(self, instruction):
        opcode_interface_task = cocotb.start_soon(self._opcode_interface.put_data(instruction.opcode.value))
        operand_interface_task = cocotb.start_soon(self._operand_interface.put_data(instruction.operand))
        await cocotb.triggers.Combine(opcode_interface_task, operand_interface_task)

    async def get(self):
        while True:
            opcode_interface_task = cocotb.start_soon(self._opcode_interface.get())
            operand_interface_task = cocotb.start_soon(self._operand_interface.get())
            return (await opcode_interface_task, await operand_interface_task)