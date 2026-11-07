from procwatch import process
from procwatch.models import Process
import procwatch.process as process_module
import pytest


def create_status_file(proc_dir, pid, name, memory=1000):
    """Create a fake Linux process status file."""

    process_dir = proc_dir / str(pid)
    process_dir.mkdir()

    status_file = process_dir / "status"
    status_file.write_text(
        f"Name:\t{name}\n"
        f"State:\tS (sleeping)\n"
        f"Pid:\t{pid}\n"
        f"PPid:\t1\n"
        f"VmRSS:\t{memory} kB\n"
        f"Threads:\t4\n"
    )


def test_get_process_status(tmp_path, monkeypatch):
    create_status_file(tmp_path, 123, "python")

    monkeypatch.setattr(process, "PROC_PATH", tmp_path)

    result = process.get_process_status(123)

    assert result["Name"] == "python"
    assert result["Pid"] == "123"
    assert result["State"] == "S (sleeping)"


def test_get_process_ids(tmp_path, monkeypatch):
    create_status_file(tmp_path, 456, "chrome")
    create_status_file(tmp_path, 123, "python")

    # Non-numeric entries should be ignored.
    (tmp_path / "self").mkdir()

    monkeypatch.setattr(process, "PROC_PATH", tmp_path)

    result = process.get_process_ids()

    assert result == [123, 456]


def test_get_process(tmp_path, monkeypatch):
    create_status_file(tmp_path, 123, "python", memory=2500)

    monkeypatch.setattr(process, "PROC_PATH", tmp_path)

    result = process.get_process(123)

    assert isinstance(result, Process)
    assert result.pid == 123
    assert result.name == "python"
    assert result.state == "S (sleeping)"
    assert result.parent_pid == 1
    assert result.memory_kb == 2500
    assert result.threads == 4


def test_get_processes(tmp_path, monkeypatch):
    create_status_file(tmp_path, 123, "python")
    create_status_file(tmp_path, 456, "chrome")

    monkeypatch.setattr(process, "PROC_PATH", tmp_path)

    result = process.get_processes()

    assert len(result) == 2
    assert [item.pid for item in result] == [123, 456]


def test_sort_by_cpu():
    processes = [
        Process(1, "python", "S", 0, 1000, 2, 10.0),
        Process(2, "chrome", "S", 0, 2000, 4, 50.0),
        Process(3, "bash", "S", 0, 500, 1, 20.0),
    ]

    result = process.sort_by_cpu(processes)

    assert [item.pid for item in result] == [2, 3, 1]


def test_sort_by_memory():
    processes = [
        Process(1, "python", "S", 0, 1000, 2),
        Process(2, "chrome", "S", 0, 3000, 4),
        Process(3, "bash", "S", 0, 500, 1),
    ]

    result = process.sort_by_memory(processes)

    assert [item.pid for item in result] == [2, 1, 3]


def test_filter_by_name():
    processes = [
        Process(1, "python", "S", 0, 1000, 2),
        Process(2, "chrome", "S", 0, 2000, 4),
        Process(3, "chrome-helper", "S", 0, 500, 1),
    ]

    result = process.filter_by_name(processes, "CHROME")

    assert [item.pid for item in result] == [2, 3]

def test_get_processes_with_cpu_usage(monkeypatch):
    processes = [
        Process(123, "python", "R", 1, 2048, 4),
        Process(456, "chrome", "S", 1, 4096, 8),
    ]

    monkeypatch.setattr(
        process_module,
        "measure_cpu_usage",
        lambda interval: (50.0, {123: 25.0, 456: 10.0}),
    )

    monkeypatch.setattr(
        process_module,
        "get_process",
        lambda pid: next(p for p in processes if p.pid == pid),
    )

    result = process_module.get_processes_with_cpu_usage(interval=0.5)

    assert len(result) == 2
    assert result[0].cpu_percent == 25.0
    assert result[1].cpu_percent == 10.0


def test_get_processes_with_cpu_usage_skips_missing_process(monkeypatch):
    monkeypatch.setattr(
        process_module,
        "measure_cpu_usage",
        lambda interval: (50.0, {123: 25.0}),
    )

    def mock_get_process(pid):
        raise ProcessLookupError

    monkeypatch.setattr(process_module, "get_process", mock_get_process)

    result = process_module.get_processes_with_cpu_usage()

    assert result == []


def test_get_processes_with_cpu_usage_skips_missing_status(monkeypatch):
    monkeypatch.setattr(
        process_module,
        "measure_cpu_usage",
        lambda interval: (50.0, {123: 25.0}),
    )

    def mock_get_process(pid):
        raise FileNotFoundError

    monkeypatch.setattr(process_module, "get_process", mock_get_process)

    result = process_module.get_processes_with_cpu_usage()

    assert result == []


def test_get_processes_with_cpu_usage_skips_invalid_process(monkeypatch):
    monkeypatch.setattr(
        process_module,
        "measure_cpu_usage",
        lambda interval: (50.0, {123: 25.0}),
    )

    def mock_get_process(pid):
        raise KeyError("Pid")

    monkeypatch.setattr(process_module, "get_process", mock_get_process)

    result = process_module.get_processes_with_cpu_usage()

    assert result == []


def test_get_process_status_missing_process(monkeypatch, tmp_path):
    monkeypatch.setattr(
        process_module,
        "PROC_PATH",
        tmp_path,
    )

    with pytest.raises(ProcessLookupError):
        process_module.get_process_status(99999)