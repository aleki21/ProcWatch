def display_processes(processes):
    """Display processes in a simple table."""

    print()
    print(
        f"{'PID':<8} "
        f"{'NAME':<20} "
        f"{'STATE':<20} "
        f"{'CPU':>8} "
        f"{'MEMORY':>12} "
        f"{'THREADS':>8}"
    )

    print("-" * 82)

    for process in processes:
        memory_mb = process.memory_kb / 1024

        print(
            f"{process.pid:<8} "
            f"{process.name:<20} "
            f"{process.state:<20} "
            f"{process.cpu_percent:>7.2f}% "
            f"{memory_mb:>9.1f} MB "
            f"{process.threads:>8}"
        )