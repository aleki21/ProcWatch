from pathlib import Path


def get_process_status(pid: int) -> dict:
    """Read basic information about a linux process."""

    status_file = Path(f"/proc/{pid}/status")

    if not status_file.exists():
        raise ProcessLookupError(f"Process {pid} does not exist")

    process_info = {}

    with status_file.open() as file:
        for line in file:
            key, value = line.split(":", 1)
            process_info[key] = value.strip()

    return process_info