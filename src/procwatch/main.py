import os

from procwatch.cpu import get_process_cpu_time


def main():
    pid = os.getpid()

    cpu_time = get_process_cpu_time(pid)

    print(f"PID: {pid}")
    print(f"CPU time: {cpu_time} ticks")


if __name__ == "__main__":
    main()