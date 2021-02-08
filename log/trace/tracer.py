#!/usr/bin/env python3

from bcc import BPF
from bcc.utils import printb
import time
from collections import defaultdict

BPF_PROGRAM = "event_monitor_ebpf.c"

def load_bpf_program():
    with open(BPF_PROGRAM, "r") as f:
        bpf = f.read()
    return bpf

bpf_text = load_bpf_program()

# initialize BPF
b = BPF(text=bpf_text)
execve_fnname = b.get_syscall_fnname("execve")
b.attach_kprobe(event=execve_fnname, fn_name="syscall__execve")
b.attach_kretprobe(event=execve_fnname, fn_name="do_ret_sys_execve")

print("%-16s %-6s %-6s %3s" % ("PCOMM", "PID", "PPID", "RET"))

class EventType(object):
    EVENT_ARG = 0
    EVENT_RET = 1

start_ts = time.time()
argv = defaultdict(list)

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    skip = False

    if event.type == EventType.EVENT_ARG:
        pass
    elif event.type == EventType.EVENT_RET:
        if event.retval != 0:
            skip = True

        if not skip:
            ppid = event.ppid if event.ppid > 0 else get_ppid(event.pid)
            ppid = b"%d" % ppid if ppid > 0 else b"?"
            printb(b"%-16s %-6d %-6s %3d" % (event.comm, event.pid,
                    ppid, event.retval))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
