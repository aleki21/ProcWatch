
from procwatch import monitor
from procwatch.models import Process


def test_run_monitor_displays_system_information(monkeypatch, capsys):
    """Test that monitoring displays system and process information."""

    process_1 = Process(
        pid=123,
        name="python",
        state="S",
        parent_pid=1,
        memory_kb=2000,
        threads=4,
    )

    monkeypatch.setattr(
        monitor,
        "measure_cpu_usage",
        lambda interval: (25.0, {123: 50.0}),
    )

    monkeypatch.setattr(
        monitor,
        "get_memory_usage",
        lambda: (5000000, 8000000, 62.5),
    )

    monkeypatch.setattr(
        monitor,
        "get_load_average",
        lambda: (0.22, 0.08, 0.02),
    )

    monkeypatch.setattr(
        monitor,
        "get_process",
        lambda pid: process_1,
    )

    monkeypatch.setattr(
        monitor.os,
        "system",
        lambda command: 0,
    )

    monkeypatch.setattr(
        monitor,
        "display_processes",
        lambda processes, limit: None,
    )

    def stop_monitor():
        raise KeyboardInterrupt

    monkeypatch.setattr(
        monitor,
        "display_processes",
        lambda processes, limit: stop_monitor(),
    )

    try:
        monitor.run_monitor()
    except KeyboardInterrupt:
        pass

    output = capsys.readouterr().out

    assert "ProcWatch — Live Monitoring" in output
    assert "25.00%" in output
    assert "62.50%" in output
    assert "0.22" in output
    assert "Processes: 1" in output


def test_run_monitor_filters_processes(monkeypatch):
    """Test that monitoring filters processes by name."""

    processes = {
        123: Process(123, "python", "S", 1, 2000, 4),
        456: Process(456, "chrome", "S", 1, 4000, 8),
    }

    monkeypatch.setattr(
        monitor,
        "measure_cpu_usage",
        lambda interval: (10.0, {123: 20.0, 456: 30.0}),
    )

    monkeypatch.setattr(
        monitor,
        "get_memory_usage",
        lambda: (1000, 2000, 50.0),
    )

    monkeypatch.setattr(
        monitor,
        "get_load_average",
        lambda: (0.1, 0.2, 0.3),
    )

    monkeypatch.setattr(
        monitor,
        "get_process",
        lambda pid: processes[pid],
    )

    monkeypatch.setattr(
        monitor.os,
        "system",
        lambda command: 0,
    )

    captured = {}

    def capture_display(displayed_processes, limit):
        captured["processes"] = displayed_processes
        captured["limit"] = limit
        raise KeyboardInterrupt

    monkeypatch.setattr(
        monitor,
        "display_processes",
        capture_display,
    )

    try:
        monitor.run_monitor(name="chrome", limit=5)
    except KeyboardInterrupt:
        pass

    result = captured["processes"]

    assert len(result) == 1
    assert result[0].name == "chrome"
    assert captured["limit"] == 5
