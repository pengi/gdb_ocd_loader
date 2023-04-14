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

# To get more packs: https://developer.arm.com/embedded/cmsis/cmsis-packs

# Add aliases for your commonly used probes or devboards such as:
# alias probe_name = python probe_setup(probe_pyocd, "target", "unique_id", "pack file")
# "unique id" and "pack file" are optional
#
# To get the unique ids of connected probes, run "pyocd list"

alias probe1 = python probe_setup(probe_pyocd, "nrf52840", "123456")
alias probe2 = python probe_setup(probe_pyocd, "stm32f767zi", "123456", "/path/to/Keil.STM32F7xx_DFP.2.15.1.pack")
alias first  = python probe_setup(probe_pyocd, "cortex_m")

define single
python probe_setup(probe_pyocd, "$arg0")
end

################################################################################
# Other extensions
################################################################################

# Load useful extensions
#
# To install:
# pip install freertos-gdb
# pip install arm-gdb
#
# For SVD files, check out:
# https://github.com/posborne/cmsis-svd
# or extract from .pack files above, which are renamed zip archives

python import freertos_gdb
python import arm_gdb
arm loadfile nrf52840  /path/to/cmsis-svd/data/Nordic/nrf52840.svd
arm loadfile stm32f7x7 /path/to/cmsis-svd/data/STMicro/STM32F7x7.svd