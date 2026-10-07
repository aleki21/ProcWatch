from pathlib import Path
import time


PROC_PATH = Path("/proc")


def get_process_cpu_time(pid: int) -> int:
    """Return the total CPU time used by a process in clock ticks."""

    stat_file = PROC_PATH / str(pid) / "stat"

    with stat_file.open() as file:
        stat = file.read()

    # The process name can contain spaces, so find the closing ')'.
    closing_paren = stat.rfind(")")
    fields = stat[closing_paren + 2:].split()

    # utime = field 14 -> index 11
    # stime = field 15 -> index 12
    utime = int(fields[11])
    stime = int(fields[12])

    return utime + stime


def get_system_cpu_time() -> int:
    """Return the total system CPU time in clock ticks."""

    stat_file = PROC_PATH / "stat"

    with stat_file.open() as file:
        for line in file:
            if line.startswith("cpu "):
                fields = line.split()

                # Use the first 8 CPU counters.
                cpu_times = [int(value) for value in fields[1:9]]

                return sum(cpu_times)

    raise RuntimeError("Could not find CPU information in /proc/stat")


def get_process_cpu_usage(pid: int, interval: float = 1.0) -> float:
    """Measure a process's CPU usage over a time interval."""

    process_start = get_process_cpu_time(pid)
    system_start = get_system_cpu_time()

    time.sleep(interval)

    process_end = get_process_cpu_time(pid)
    system_end = get_system_cpu_time()

    process_delta = process_end - process_start
    system_delta = system_end - system_start

    if system_delta == 0:
        return 0.0

    return (process_delta / system_delta) * 100