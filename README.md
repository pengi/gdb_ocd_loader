PyOCD is a debbuging tool that can act as a gdb server. This shows how to set it up to automatically start from within gdb

## Install

Assume running ubuntu 22.04. Tune the commands to match your setup. Haven't tested on a clean install, so PATH and PYTHONPATH might need tuning.

If `gdb-multiarch` isn't available, `arm-none-eabi-gdb-py` should probably work too.

```sh
apt install gdb-multiarch
python3 -m pip install --pre -U git+https://github.com/pyocd/pyOCD.git@develop
python3 -m pip install arm-gdb
python3 -m pip pip install freertos-gdb
```

## Configure PyOCD

This repository contains files that sets up integration between pyocd and gdb, so that pyocd can be launched from within gdb.

Easiest is to clone this repo to somewhere on your file system, copy `gdbinit_template.gdb` to `~/.gdbinit` and update with local configuration.

Or you can use the scripts here as template to set your own system up as you want.

## gdb usage

To connect to a probe, run the command specified as alias, followed by `connect`:
```
(gdb) probe1
(gdb) connect
```

pyocd (or the gdb server specified) will start and auto connect.

To reconnect, which is useful when running freertos and elf file needs to reload in pyocd too, type `connect` again, and it will reconnect:
```
(gdb) load
(gdb) connect
```

Resetting the device, it is usually expected that the device is halted after reset. The command to reset in pyocd is `monitor reset halt`, which is added as an alias above:

```
(gdb) res
```

The commonly used `mon reset` when using for example `JLinkGDBServer` or `st-util` will therefore not behave as expected when using `pyocd`.

When developing, the target `.elf` file is usually in the same directory, and `make myfile.elf` rebuilds it, then there is a shortcut:
```
(gdb) reload
```

This will disconnect the probe, rebuild the software, flash it and reconnect.

## OS aware debugging

Since running pyocd with loaded elf file, while running FreeRTOS, it is possible to list and inspect threads:

```
(gdb) info threads
...
(gdb) thread apply all bt
...
```

To list and switch between different FreeRTOS tasks (gdb calls them threads) and look at the stack at each Task. This needs the elf file to be loaded by pyocd, which is the main reason for the loader mentioned here.


## arm-gdb and freertos-gdb

Two useful tools to first inspect the ARM System Control Block and NVIC registers

```
(gdb) arm scb
...
(gdb) arm nvic
```

More information at: https://pypi.org/project/arm-gdb/

And
```
(gdb) freertos queue
...
```

More information at: https://pypi.org/project/freertos-gdb/

## Add support for more CPUs

PyOCD includes support for multiple microcontrollers. But they are far from all. To support more in pyocd, packs can be downloaded and used. They are available here:

https://developer.arm.com/embedded/cmsis/cmsis-packs

Download the pack, and refer to it from the probe configuration in `.gdbinit`

To add support for the device to read peripherals in `arm-gdb`, an `.svd` file is needed. Many can be found by checking out the develop version of:

https://github.com/ARM-software/CMSIS_5

But `.svd` files are parts of the `.pack`. The `.pack` is simply a renamed ZIP archive, so just unpack the `.svd` files you require from the pack file and refer to it from arm-gdb. Unfortunately arm-gdb doesn't support unpacking the `.pack` file (yet?).