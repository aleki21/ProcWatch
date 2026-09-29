from pathlib import Path

from procwatch.models import Process


PROC_PATH = Path("/proc")


def get_process_status(pid: int) -> dict:
    """Read basic information about a Linux process."""

    status_file = PROC_PATH / str(pid) / "status"

    if not status_file.exists():
        raise ProcessLookupError(f"Process {pid} does not exist")

    process_info = {}

    with status_file.open() as file:
        for line in file:
            key, value = line.split(":", 1)
            process_info[key] = value.strip()

    return process_info


def get_process_ids() -> list[int]:
    """Return the PIDs of all currently running processes."""

    process_ids = []

    for entry in PROC_PATH.iterdir():
        if entry.name.isdigit():
            process_ids.append(int(entry.name))

    return sorted(process_ids)


def get_process(pid: int) -> Process:
    """Return structured information about a process."""

    status = get_process_status(pid)

    return Process(
        pid=int(status["Pid"]),
        name=status["Name"],
        state=status["State"],
        parent_pid=int(status["PPid"]),
        memory_kb=int(status["VmRSS"].split()[0]),
        threads=int(status["Threads"]),
    )