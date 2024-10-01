################################################################################
# Loaad gdb_pycd integration
################################################################################

# Update only hte path in this section
python import os
python pyocd_gdb_integration_path = os.environ['HOME'] + '/path/to/gdb_pyocd_integration'
python exec(compile(open(pyocd_gdb_integration_path + '/gdb_init.py', "rb").read(), 'gdb_init.py', "exec"))

# Enable pretty print, if wanted
set print pretty on

# Useful aliases for the integration
alias connect = python probe_start()
alias res     = mon reset halt

# reload command is useful for auto rebuilding, but adds dependency on make and
# target name. It is expected to stand in the directory of where the loaded file
# is built, and will rebuild using: make -j32 filename.elf
alias reload  = python reload()



################################################################################
# Probe configuraiton
################################################################################

# Add aliases for your commonly used probes or devboards such as:
# alias probe_name = python probe_setup(probe_openocd, "interface", "target", "optional extra commands")

# 

# Example probe configurations:

# Select a signle nrf board
alias nrf    = python probe_setup(probe_openocd, "jlink", "nrf52")

# Select a predefined nrf board. Serial can be fetched using "pyocd list"
alias nrf1   = python probe_setup(probe_openocd, "jlink", "nrf52", "jlink serial 123456789")

# To specify probe and device on command line

define probe
python probe_setup(probe_openocd, "$arg0", "$arg1")
end

################################################################################
# Other extensions
################################################################################

# Load useful extensions
#
# To install:
# pip install arm-gdb
# pip install freertos-gdb
#
# For SVD files, check out:
# https://github.com/posborne/cmsis-svd
# or extract from .pack files above, which are renamed zip archives

# Uncomment to use:

# python import arm_gdb
# python import freertos_gdb
# arm loadfile nrf52840  /path/to/cmsis-svd/data/Nordic/nrf52840.svd
# arm loadfile stm32f7x7 /path/to/cmsis-svd/data/STMicro/STM32F7x7.svd
