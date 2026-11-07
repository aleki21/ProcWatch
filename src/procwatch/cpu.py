
from dataclasses import dataclass
from pathlib import Path
import time


PROC_PATH = Path("/proc")


@dataclass
class CpuSnapshot:
    """CPU counters captured at a specific point in time."""

    system_total: int
    system_idle: int
    processes: dict[int, int]


def get_process_cpu_time(pid: int) -> int:
    """Return total CPU time used by a process in clock ticks."""

    stat_file = PROC_PATH / str(pid) / "stat"

    with stat_file.open() as file:
        stat = file.read()

    closing_paren = stat.rfind(")")
    fields = stat[closing_paren + 2:].split()

    utime = int(fields[11])
    stime = int(fields[12])

    return utime + stime


def get_system_cpu_snapshot() -> tuple[int, int]:
    """Return total and idle system CPU ticks."""

    stat_file = PROC_PATH / "stat"

    with stat_file.open() as file:
        for line in file:
            if line.startswith("cpu "):
                fields = line.split()
                cpu_times = [int(value) for value in fields[1:9]]

                total = sum(cpu_times)
                idle = cpu_times[3] + cpu_times[4]

                return total, idle

    raise RuntimeError("Could not find CPU information in /proc/stat")


def get_cpu_snapshot() -> CpuSnapshot:
    """Capture system and process CPU counters."""

    system_total, system_idle = get_system_cpu_snapshot()

    processes = {}

    for entry in PROC_PATH.iterdir():
        if not entry.name.isdigit():
            continue

        pid = int(entry.name)

        try:
            processes[pid] = get_process_cpu_time(pid)
        except (FileNotFoundError, ProcessLookupError):
            continue

    return CpuSnapshot(
        system_total=system_total,
        system_idle=system_idle,
        processes=processes,
    )


def calculate_cpu_usage(
    previous: CpuSnapshot,
    current: CpuSnapshot,
) -> tuple[float, dict[int, float]]:
    """Calculate system and individual process CPU usage."""

    system_delta = current.system_total - previous.system_total

    if system_delta <= 0:
        return 0.0, {}

    idle_delta = current.system_idle - previous.system_idle

    system_usage = (
        (system_delta - idle_delta) / system_delta
    ) * 100

    process_usage = {}

    for pid, current_time in current.processes.items():
        if pid not in previous.processes:
            continue

        process_delta = current_time - previous.processes[pid]

        if process_delta < 0:
            continue

        process_usage[pid] = (
            process_delta / system_delta
        ) * 100

    return system_usage, process_usage


def measure_cpu_usage(
    interval: float = 1.0,
) -> tuple[float, dict[int, float]]:
    """Measure system and process CPU usage over an interval."""

    previous = get_cpu_snapshot()

    time.sleep(interval)

    current = get_cpu_snapshot()

    return calculate_cpu_usage(previous, current)
