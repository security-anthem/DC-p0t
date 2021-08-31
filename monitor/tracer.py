#!/usr/bin/env python3

from bcc import BPF
from bcc.utils import printb
import time
from collections import defaultdict
from time import strftime

BPF_PROGRAM = "monitor/trace/event_monitor_ebpf.c"

def load_bpf_program():
    with open(BPF_PROGRAM, "r") as f:
        bpf = f.read()
    return bpf

bpf_text = load_bpf_program()
bpf_text = bpf_text.replace("MAXARG", "20")

# initialize BPF
b = BPF(text=bpf_text)
execve_fnname = b.get_syscall_fnname("execve")
b.attach_kprobe(event=execve_fnname, fn_name="syscall__execve")
b.attach_kretprobe(event=execve_fnname, fn_name="do_ret_sys_execve")

# header
print("%-9s" % ("TIME"), end="")
print("%-8s" % ("TIME(s)"), end="")
print("%-6s" % ("UID"), end="")
print("%-16s %-6s %-6s %3s %s" % ("PCOMM", "PID", "PPID", "RET", "ARGS"))

class EventType(object):
    EVENT_ARG = 0
    EVENT_RET = 1

start_ts = time.time()
argv = defaultdict(list)

def get_ppid(pid):
    try:
        with open("/proc/%d/status" % pid) as status:
            for line in status:
                if line.statuswith("PPid"):
                    return int (line.split()[1])
    except IOError:
        pass
    return 0

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    skip = False

    if event.type == EventType.EVENT_ARG:
        argv[event.pid].append(event.argv)
    elif event.type == EventType.EVENT_RET:
        if event.retval != 0:
            skip = True

        if not skip:
            printb(b"%-9s" % strftime("%H:%M:%S").encode('ascii'), nl="")
            printb(b"%-8.3f" % (time.time() - start_ts), nl="")
            printb(b"%-6d" % event.uid, nl="")
            ppid = event.ppid if event.ppid > 0 else get_ppid(event.pid)
            ppid = b"%d" % ppid if ppid > 0 else b"?"
            argv_text = b' '.join(argv[event.pid]).replace(b'\n', b'\\n')
            printb(b"%-16s %-6d %-6s %3d %s" % (event.comm, event.pid,
                    ppid, event.retval, argv_text))

        try:
            del(argv[event.pid])
        except Exception:
            pass

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
