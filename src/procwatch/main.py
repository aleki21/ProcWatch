import argparse

from procwatch.monitor import run_monitor


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

    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Seconds between measurements",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        run_monitor(
            interval=args.interval,
            sort_by=args.sort,
            limit=args.limit,
            name=args.name,
        )
    except KeyboardInterrupt:
        print("\nProcWatch stopped.")


if __name__ == "__main__":
    main()
