from procwatch.display import display_processes
from procwatch.process import get_processes


def main():
    processes = get_processes()

    print(f"ProcWatch — {len(processes)} processes detected")

    display_processes(processes)


if __name__ == "__main__":
    main()