import ctypes

from pvm.protocols.pcie_transaction_layer_packet.header.pcie_transaction_layer_packet_header import _PCIeTransactionLayerPacket3DWHeader, _PCIeTransactionLayerPacket4DWHeader

class _PCIeTransactionLayerPacketWith3DWHeader(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('header', _PCIeTransactionLayerPacket3DWHeader),
        ('payload', 1025 * ctypes.c_uint32)
    ]

class _PCIeTransactionLayerPacketWith4DWHeader(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('header', _PCIeTransactionLayerPacket4DWHeader),
        ('payload', 1025 * ctypes.c_uint32)
    ]

class _PCIeTransactionLayerPacket(ctypes.BigEndianUnion):
    _pack_ = 1
    _fields_ = [
        ('with_3dw_header', _PCIeTransactionLayerPacketWith3DWHeader),
        ('with_4dw_header', _PCIeTransactionLayerPacketWith4DWHeader)
    ]

class PCIeTransactionLayerPacket:
    def __init__(self):
        self._packet = _PCIeTransactionLayerPacket()

    @property
    def packet(self):
        if self._packet.with_4dw_header.header.common.fmt_header_length:
            return self._packet.with_4dw_header
        return self._packet.with_3dw_header

    @property
    def header(self):
        return self.packet.header

    @property
    def bytes(self):
        return bytes(self._packet)

    def get_bytes(self, offset, length):
        source = ctypes.addressof(self._packet) + offset
        return self.bytes[offset : offset + length]

    def copy_to(self, offset, source):
        destination = ctypes.addressof(self._packet) + offset
        ctypes.memmove(destination, source, len(source))