import argparse

from procwatch.display import display_processes
from procwatch.process import (
    filter_by_name,
    get_processes_with_cpu_usage,
    sort_by_cpu,
    sort_by_memory,
)


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="ProcWatch - Linux process monitoring tool"
    )

    parser.add_argument(
        "--sort",
        choices=["cpu", "memory"],
        default="cpu",
        help="Sort processes by CPU or memory",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of processes to display",
    )

    parser.add_argument(
        "--name",
        type=str,
        help="Filter processes by name",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    print("Measuring CPU usage...")

    processes = get_processes_with_cpu_usage()

    if args.name:
        processes = filter_by_name(processes, args.name)

    if args.sort == "cpu":
        processes = sort_by_cpu(processes)
    else:
        processes = sort_by_memory(processes)

    print()
    print(f"ProcWatch — {len(processes)} processes")

    display_processes(
        processes,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()