import os

from procwatch.process import get_process_status


def main():
    pid = os.getpid()

    process = get_process_status(pid)

    print(f"Process: {process['Name']}")
    print(f"PID: {process['Pid']}")
    print(f"Parent PID: {process['PPid']}")
    print(f"State: {process['State']}")
    print(f"Memory: {process['VmRSS']}")
    print(f"Threads: {process['Threads']}")


if __name__ == "__main__":
    main()