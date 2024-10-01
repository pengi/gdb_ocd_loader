import random
import os
import subprocess as sp
import atexit

probe_current = None

class Probe:
    REMOTE_COMMAND='remote'
    
    def __init__(self, id=None):
        self.id = id
        self.process = None
        
    def _do_start(self, port):
        raise Exception('initializing generic Probe class')
        
    def _do_stop(self):
        try:
            gdb.execute("detach")
        except:
            pass

    def start(self):
        if self.process is not None:
            self.stop()
        port = random.randint(10000, 20000)
        self.process = self._do_start(port)
        gdb.execute(f"target {self.REMOTE_COMMAND} localhost:{port}")
    
    def stop(self):
        if self.process is not None:
            self._do_stop()
            try:
                self.process.wait(timeout=2.0)
            except:
                self.process.terminate()
                print("NOTE: GDB server didn't stop, terminating")
        self.process = None

class probe_openocd(Probe):
    REMOTE_COMMAND='extended-remote'
    
    def __init__(self, interface, target, id=None, transport='swd', debug_level=1):
        super().__init__(id=id)
        self.interface = interface
        self.target = target
        self.transport = transport
        self.debug_level = debug_level
        
    def _do_start(self, port):
        script=f"""
        debug_level {self.debug_level}
        source [find interface/{self.interface}.cfg]
        transport select {self.transport}
        source [find target/{self.target}.cfg]
        gdb_port {port}
        tcl_port disabled
        telnet_port disabled
        $_TARGETNAME configure -rtos auto
        """
        
        command = ['openocd']
        for line in (l.strip() for l in script.splitlines() if l.strip() != ""):
            command += ['-c', line]

        return sp.Popen(command, start_new_session=True)

    def _do_stop(self):
        try:
            gdb.execute('mon shutdown')
            gdb.execute("detach")
        except:
            pass

class probe_pyocd(Probe):
    def __init__(self, target, id=None, pack=None):
        super().__init__(id=id)
        self.target = target
        self.pack = pack
    
    def _do_start(self, port):
        args = []

        try:
            filename = gdb.objfiles()[0].filename
            args += ['--elf', filename]
        except:
            pass

        if self.pack is not None:
            args += ['--pack', os.path.expanduser(self.pack)]

        if id is not None:
            args += ['-u', str(self.id)]

        return sp.Popen([
            'python', '-m', 'pyocd', 'gdbserver',
            '--config', pyocd_gdb_integration_path + '/pyocd_config.yml',
            '--script', pyocd_gdb_integration_path + '/pyocd_user.py',
            '-t', self.target,
            '-p', str(port)
        ] + args, start_new_session=True)


class probe_stlink(Probe):
    def __init__(self, target, id=None):
        super().__init__(id=id)
        self.target = target
    
    def _do_start(self, port):
        return sp.Popen([
            'st-util',
            '--serial', str(self.id),
            '-p', str(self.port)
        ], start_new_session=True)


class probe_jlink(Probe):
    def __init__(self, target, id=None):
        super().__init__(id=id)
        self.target = target
    
    def _do_start(self, port):
        return sp.Popen([
            'JLinkGDBServer',
            '-nogui',
            '-if', 'swd',
            '-speed', '4000',
            '-localhostonly',
            '-select', 'usb='+str(self.id),
            '-port', str(port),
            '-device', self.target,
            '-singlerun'
        ], stdout=sp.DEVNULL, start_new_session=True)


def get_filename():
    try:
        return os.path.relpath(gdb.objfiles()[0].filename)
    except:
        return None


def probe_setup(probe, *args, **kwargs):
    global probe_current
    
    if probe_current is not None:
        probe_current.stop()
    probe_current = probe(*args, **kwargs)

def probe_start():
    global probe_current
    probe_current.start()


def probe_stop():
    global probe_current
    probe_current.stop()

def reload():
    global probe_current
    if probe_current is None:
        print("No probe selected")
        return
    probe_stop()
    gdb.execute("make -j32 " + get_filename())
    probe_start()
    gdb.execute("load")
    gdb.execute("monitor reset halt")

def at_exit_handler():
    probe_stop()

atexit.register(at_exit_handler)
