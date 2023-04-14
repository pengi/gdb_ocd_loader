import random
import os
import subprocess as sp
import atexit

probe_config = {}
probe_process = None


def probe_pyocd(port, target, id=None, pack=None):
    args = []

    try:
        filename = gdb.objfiles()[0].filename
        args += ['--elf', filename]
    except:
        pass

    if pack is not None:
        args += ['--pack', os.path.expanduser(pack)]

    if id is not None:
        args += ['-u', str(id)]

    return sp.Popen([
        'python', '-m', 'pyocd', 'gdbserver',
        '--config', pyocd_gdb_integration_path + '/pyocd_config.yml',
        '--script', pyocd_gdb_integration_path + '/pyocd_user.py',
        '-t', target,
        '-p', str(port)
    ] + args, start_new_session=True)


def probe_stlink(port, id):
    return sp.Popen([
        'st-util',
        '--serial', str(id),
        '-p', str(port)
    ], start_new_session=True)


def probe_jlink(port, target, id):
    return sp.Popen([
        'JLinkGDBServer',
        '-nogui',
        '-if', 'swd',
        '-speed', '8000',
        '-localhostonly',
        '-select', 'usb='+str(id),
        '-port', str(port),
        '-device', target,
        '-singlerun'
    ], stdout=sp.DEVNULL, start_new_session=True)


def get_filename():
    try:
        return os.path.basename(gdb.objfiles()[0].filename)
    except:
        return None


def probe_setup(start_func, *args, **kwargs):
    global probe_config
    global probe_process
    probe_stop()
    probe_process = None
    probe_config['start_func'] = start_func
    probe_config['args'] = args
    probe_config['kwargs'] = kwargs


def probe_start():
    global probe_process
    global probe_config
    probe_stop()
    port = random.randint(10000, 20000)
    probe_process = probe_config['start_func'](
        port,
        *probe_config['args'],
        **probe_config['kwargs']
    )
    gdb.execute("target remote localhost:%d" % (port,))


def probe_stop():
    global probe_process
    if probe_process is not None:
        try:
            gdb.execute("detach")
        except:
            pass
        try:
            probe_process.wait(timeout=3.0)
        except:
            probe_process.terminate()
        probe_process = None


def reload():
    global probe_config
    probe_stop()
    gdb.execute("make -j32 " + get_filename())
    probe_start()
    gdb.execute("load")
    gdb.execute("monitor reset halt")
    gdb.execute("continue")


def at_exit_handler():
    probe_stop()


atexit.register(at_exit_handler)
