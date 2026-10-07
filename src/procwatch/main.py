import os

from procwatch.cpu import get_process_cpu_usage


def main():
    pid = os.getpid()

    cpu_usage = get_process_cpu_usage(pid)

    print(f"PID: {pid}")
    print(f"CPU usage: {cpu_usage:.2f}%")


if __name__ == "__main__":
    main()