# GDB OCD loader

Automatically start gdb-server from within GDB

When developing for ARM Cortex-M microcontrollers, it's often needed to restart
the GDB server. This is a helper to manage the gdb server instances from within
gdb.

Setup your `.gdbinit` with the probes available, then simply use command
`connect` to start the gdb server, and connect to it.

Command `reload` will the recompile your application, reload the target and
restart the gdb server.

## Supported gdb-servers

Multiple gdb-servers are supported:

- `pyOCD`   - generic interface which is RTOS aware. Originally developed for.
- `openocd` - currently preferred interface. RTOS aware too. Supports most
              probes.
- `jlink`   - Not RTOS-aware, but commonly used. If application doesn't use RTOS
              threads, it may be a good choice.
- `st-link` - Used for stm32 targets using the st-link. However, also supported
              by openocd

## Install

Install a version of gdb that supports python. `gdb-multiarch` is recommended,
but `arm-none-eabi-gdb-py` should work too.

On Ubuntu 22.04:
```sh
apt install gdb-multiarch
```

Then clone this repo in a location of choice, for example in the home directory:

```sh
cd ~
git clone https://github.com/pengi/gdb_ocd_loader.git
```

Use the `gdbinit_template.gdb` in this repo as template for your `~/.gdbinit` to
load gdb_ocd_loader.

## Configuration

Follow instructions in `gdbinit_template.gdb`

The probes available are:
### OpenOCD
```
alias my_probe = python probe_setup(probe_openocd, "interface", "target", "command")
```

`"command"` is optional, and will add commands to the openocd script. Useful for
selecting a sepcific interface, for example `jlink serial 123456789`.

`"command"` can be an array to specify multiple commands.

### pyOCD
```
alias my_probe = python probe_setup(probe_pyocd, "target", "id", "pack file")
```

### st-link
```
alias my_probe = python probe_setup(probe_stlink, "target", "id")
```

### jlink
```
alias my_probe = python probe_setup(probe_pyocd, "target", "id")
```


## gdb usage

To connect to a probe, run the command specified as alias, in this example
`nrf`, followed by `connect`:
```
(gdb) nrf
(gdb) connect
```

openocd (or the gdb server specified) will start and auto connect.

Some gdb-servers (in particular pyocd), needs the elf file when starting, to
identify RTOS threads. Therefore, restart is recommended when reloading.
`connect` will automatically disconnect previous connection before reconneting.

```
(gdb) load
(gdb) connect
```

Resetting the device, it is usually expected that the device is halted after
reset. The command to reset in pyocd is `monitor reset halt`, which is added as
an alias above:

```
(gdb) res
```

When developing, the target `.elf` file is usually in the same directory, and
`make myfile.elf` rebuilds it, then there is a shortcut:
```
(gdb) reload
```

This will disconnect the probe, rebuild the software, flash it and reconnect.

## OS aware debugging

If using an RTOS aware gdb-server, for example `openocd` or `pyocd`, it is
possible to list RTOS tasks and inspect RTOS tasks:

```
(gdb) info threads
...
(gdb) thread apply all bt
...
```

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
