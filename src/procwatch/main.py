from procwatch.process import get_process


def main():
    process = get_process(1)

    print(process)
    print(process.name)
    print(process.pid)
    print(process.memory_kb)


if __name__ == "__main__":
    main()