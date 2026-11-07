from procwatch.display import display_processes
from procwatch.models import Process


def test_display_processes(capsys):
    processes = [
        Process(
            pid=123,
            name="python",
            state="R",
            parent_pid=1,
            memory_kb=2048,
            threads=4,
            cpu_percent=15.5,
        )
    ]

    display_processes(processes)

    captured = capsys.readouterr()

    assert "PID" in captured.out
    assert "NAME" in captured.out
    assert "CPU" in captured.out
    assert "MEMORY" in captured.out
    assert "THREADS" in captured.out

    assert "123" in captured.out
    assert "python" in captured.out
    assert "15.50%" in captured.out
    assert "2.0 MB" in captured.out


def test_display_processes_respects_limit(capsys):
    processes = [
        Process(123, "python", "R", 1, 2048, 4, 15.5),
        Process(456, "chrome", "S", 1, 4096, 8, 10.0),
    ]

    display_processes(processes, limit=1)

    captured = capsys.readouterr()

    assert "python" in captured.out
    assert "chrome" not in captured.out
    