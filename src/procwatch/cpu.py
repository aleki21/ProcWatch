from pathlib import Path
import time


PROC_PATH = Path("/proc")


def get_process_cpu_time(pid: int) -> int:
    """Return the total CPU time used by a process in clock ticks."""

    stat_file = PROC_PATH / str(pid) / "stat"

    with stat_file.open() as file:
        stat = file.read()

    closing_paren = stat.rfind(")")
    fields = stat[closing_paren + 2:].split()

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

                cpu_times = [int(value) for value in fields[1:9]]

                return sum(cpu_times)

    raise RuntimeError("Could not find CPU information in /proc/stat")


def get_cpu_snapshot() -> dict[int, int]:
    """Return CPU times for all currently running processes."""

    snapshot = {}

    for entry in PROC_PATH.iterdir():
        if not entry.name.isdigit():
            continue

        pid = int(entry.name)

        try:
            snapshot[pid] = get_process_cpu_time(pid)
        except (FileNotFoundError, ProcessLookupError):
            # The process may have exited while we were reading it.
            continue

    return snapshot


def calculate_cpu_usage(
    previous: dict[int, int],
    current: dict[int, int],
    system_delta: int,
) -> dict[int, float]:
    """Calculate CPU usage for each process."""

    if system_delta <= 0:
        return {}

    usage = {}

    for pid, current_time in current.items():
        if pid not in previous:
            continue

        process_delta = current_time - previous[pid]

        if process_delta < 0:
            continue

        usage[pid] = (process_delta / system_delta) * 100

    return usage


def measure_cpu_usage(interval: float = 1.0) -> dict[int, float]:
    """Measure CPU usage for all processes over an interval."""

    previous_processes = get_cpu_snapshot()
    previous_system = get_system_cpu_time()

    time.sleep(interval)

    current_processes = get_cpu_snapshot()
    current_system = get_system_cpu_time()

    system_delta = current_system - previous_system

    return calculate_cpu_usage(
        previous_processes,
        current_processes,
        system_delta,
    )