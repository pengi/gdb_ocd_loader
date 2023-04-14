# Normally, pack files skips the system control space and peripherals when
# specifying memory map. Those areas are useful to access with debugger, so add
# them manulally to the memory map

def will_connect(board):
    target.memory_map.add_region(DeviceRegion(
        name="Peripheral",
        start=0x40000000,
        length=0x20000000,
        access='rw'
    ))
    target.memory_map.add_region(DeviceRegion(
        name="PPB",
        start=0xE0000000,
        length=0x20000000,
        access='rw'
    ))
