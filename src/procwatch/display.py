def display_processes(processes):
    """Display processes in a simple table."""

    print()
    print(f"{'PID':<8} {'NAME':<20} {'STATE':<20} {'MEMORY':>12} {'THREADS':>8}")
    print("-" * 72)

    for process in processes:
        memory_mb = process.memory_kb / 1024

        print(
            f"{process.pid:<8} "
            f"{process.name:<20} "
            f"{process.state:<20} "
            f"{memory_mb:>9.1f} MB "
            f"{process.threads:>8}"
        )