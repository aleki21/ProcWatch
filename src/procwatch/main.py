from procwatch.process import get_processes_with_cpu_usage


def main():
    print("Measuring CPU usage...")

    processes = get_processes_with_cpu_usage()

    processes.sort(
        key=lambda process: process.cpu_percent,
        reverse=True,
    )

    print()
    print(f"ProcWatch — {len(processes)} processes measured")
    print()

    print(
        f"{'PID':<8} "
        f"{'NAME':<25} "
        f"{'CPU':>8} "
        f"{'MEMORY':>12} "
        f"{'THREADS':>8}"
    )

    print("-" * 66)

    for process in processes[:20]:
        memory_mb = process.memory_kb / 1024

        print(
            f"{process.pid:<8} "
            f"{process.name:<25} "
            f"{process.cpu_percent:>7.2f}% "
            f"{memory_mb:>9.1f} MB "
            f"{process.threads:>8}"
        )


if __name__ == "__main__":
    main()