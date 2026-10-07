from pathlib import Path


PROC_PATH = Path("/proc")


def get_process_cpu_time(pid: int) -> int:
    """Return the total CPU time used by a process in clock ticks."""

    stat_file = PROC_PATH / str(pid) / "stat"

    with stat_file.open() as file:
        stat = file.read()

    # The process name can contain spaces, so find the closing ')'
    # rather than simply splitting the entire string.
    closing_paren = stat.rfind(")")
    fields = stat[closing_paren + 2:].split()

    # Fields after the process name start at field 3.
    # utime = field 14 -> index 11
    # stime = field 15 -> index 12
    utime = int(fields[11])
    stime = int(fields[12])

    return utime + stime