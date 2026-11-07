from pathlib import Path

PROC_PATH = Path("/proc")


def get_memory_info() -> dict[str, int]:
    """Return memory information from /proc/meminfo in kB."""

    meminfo_file = PROC_PATH / "meminfo"
    memory = {}

    with meminfo_file.open() as file:
        for line in file:
            key, value = line.split(":", 1)
            parts = value.strip().split()

            if not parts:
                continue

            memory[key] = int(parts[0])

    return memory


def get_memory_usage() -> tuple[int, int, float]:
    """Return used memory, total memory and usage percentage."""

    memory = get_memory_info()

    total = memory["MemTotal"]
    available = memory["MemAvailable"]

    used = total - available
    percentage = (used / total) * 100

    return used, total, percentage


def get_load_average() -> tuple[float, float, float]:
    """Return system load averages for 1, 5 and 15 minutes."""

    loadavg_file = PROC_PATH / "loadavg"

    with loadavg_file.open() as file:
        values = file.read().split()

    load_1 = float(values[0])
    load_5 = float(values[1])
    load_15 = float(values[2])

    return load_1, load_5, load_15


if __name__ == "__main__":
    print("Memory usage:", get_memory_usage())
    print("Load average:", get_load_average())