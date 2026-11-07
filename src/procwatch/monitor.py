import os

from procwatch.cpu import measure_cpu_usage
from procwatch.display import display_processes
from procwatch.process import (
    filter_by_name,
    get_process,
    sort_by_cpu,
    sort_by_memory,
)
from procwatch.system import get_memory_usage, get_load_average


def run_monitor(
    interval: float = 2.0,
    sort_by: str = "cpu",
    limit: int = 20,
    name: str | None = None,
):
    """Continuously monitor the system and processes."""

    while True:
        system_cpu, cpu_usage = measure_cpu_usage(interval)

        used_memory, total_memory, memory_percent = get_memory_usage()

        load_1, load_5, load_15 = get_load_average()

        processes = []

        for pid, cpu_percent in cpu_usage.items():
            try:
                process = get_process(pid)
                process.cpu_percent = cpu_percent
                processes.append(process)

            except (ProcessLookupError, KeyError):
                continue

        if name:
            processes = filter_by_name(processes, name)

        if sort_by == "cpu":
            processes = sort_by_cpu(processes)
        else:
            processes = sort_by_memory(processes)

        os.system("clear")

        print("ProcWatch — Live Monitoring")
        print("=" * 66)

        print(f"CPU:        {system_cpu:>6.2f}%")
        print(
            f"Memory:    {used_memory / 1024:>6.1f} / "
            f"{total_memory / 1024:.1f} MB "
            f"({memory_percent:.2f}%)"
        )

        print(
            f"Load Avg:   {load_1:.2f} "
            f"{load_5:.2f} "
            f"{load_15:.2f} "
            "(1m, 5m, 15m)"
        )

        print(f"Processes: {len(processes)}")

        display_processes(processes, limit=limit)