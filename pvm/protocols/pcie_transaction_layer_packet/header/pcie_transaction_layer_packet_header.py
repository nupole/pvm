import ctypes

from pvm.protocols.pcie_transaction_layer_packet.header.common.pcie_transaction_layer_packet_header_common import _PCIeTransactionLayerPacketHeaderCommon

class _PCIeTransactionLayerPacket3DWHeader(ctypes.BigEndianUnion):
    _pack_ = 1
    _fields_ = [
        ('common', _PCIeTransactionLayerPacketHeaderCommon),
        ('reserved', 2 * ctypes.c_uint32)
    ]

class _PCIeTransactionLayerPacket4DWHeader(ctypes.BigEndianUnion):
    _pack_ = 1
    _fields_ = [
        ('common', _PCIeTransactionLayerPacketHeaderCommon),
        ('reserved', 3 * ctypes.c_uint32)
    ]