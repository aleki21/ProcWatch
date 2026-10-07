def display_processes(processes, limit=20):
    """Display processes in a table."""

    print()

    print(
        f"{'PID':<8}"
        f"{'NAME':<25}"
        f"{'CPU':>8}"
        f"{'MEMORY':>12}"
        f"{'THREADS':>8}"
    )

    print("-" * 66)

    for process in processes[:limit]:
        memory_mb = process.memory_kb / 1024

        print(
            f"{process.pid:<8}"
            f"{process.name:<25}"
            f"{process.cpu_percent:>7.2f}%"
            f"{memory_mb:>9.1f} MB"
            f"{process.threads:>8}"
        )