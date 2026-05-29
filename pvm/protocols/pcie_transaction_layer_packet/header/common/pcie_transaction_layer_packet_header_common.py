import ctypes

class _PCIeTransactionLayerPacketHeaderCommon(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fmt_tlp_prefix', ctypes.c_uint8, 1),
        ('fmt_data_indicator', ctypes.c_uint8, 1),
        ('fmt_header_length', ctypes.c_uint8, 1),
        ('type', ctypes.c_uint8, 5),
        ('reserved', ctypes.c_uint8, 1),
        ('tc', ctypes.c_uint8, 3),
        ('reserved', ctypes.c_uint8, 1),
        ('attr_id_based_ordering', ctypes.c_uint8, 1),
        ('reserved', ctypes.c_uint8, 1),
        ('th', ctypes.c_uint8, 1),
        ('td', ctypes.c_uint8, 1),
        ('ep', ctypes.c_uint8, 1),
        ('attr_relaxed_ordering', ctypes.c_uint8, 1),
        ('attr_no_snoop', ctypes.c_uint8, 1),
        ('at', ctypes.c_uint8, 2),
        ('length', ctypes.c_uint16, 10)
    ]