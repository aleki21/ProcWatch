
from procwatch.cpu import CpuSnapshot, calculate_cpu_usage
from procwatch import cpu


def test_calculate_cpu_usage():
    """Test system and individual process CPU usage."""

    previous = CpuSnapshot(
        system_total=1000,
        system_idle=800,
        processes={
            123: 100,
            456: 200,
        },
    )

    current = CpuSnapshot(
        system_total=1100,
        system_idle=850,
        processes={
            123: 120,
            456: 210,
            789: 50,
        },
    )

    system_cpu, process_cpu = calculate_cpu_usage(previous, current)

    assert system_cpu == 50.0
    assert process_cpu[123] == 20.0
    assert process_cpu[456] == 10.0

    # New processes have no previous snapshot.
    assert 789 not in process_cpu


def test_calculate_cpu_usage_with_no_system_delta():
    """Test handling of snapshots with no CPU counter change."""

    previous = CpuSnapshot(
        system_total=1000,
        system_idle=800,
        processes={123: 100},
    )

    current = CpuSnapshot(
        system_total=1000,
        system_idle=800,
        processes={123: 120},
    )

    system_cpu, process_cpu = calculate_cpu_usage(previous, current)

    assert system_cpu == 0.0
    assert process_cpu == {}


def test_calculate_cpu_usage_with_negative_process_delta():
    """Test that negative process counter changes are ignored."""

    previous = CpuSnapshot(
        system_total=1000,
        system_idle=800,
        processes={123: 200},
    )

    current = CpuSnapshot(
        system_total=1100,
        system_idle=850,
        processes={123: 100},
    )

    system_cpu, process_cpu = calculate_cpu_usage(previous, current)

    assert system_cpu == 50.0
    assert 123 not in process_cpu


def test_get_process_cpu_time(tmp_path, monkeypatch):
    """Test reading CPU ticks from a process stat file."""

    process_dir = tmp_path / "123"
    process_dir.mkdir()

    stat_file = process_dir / "stat"

    # The process name contains spaces and parentheses.
    stat_file.write_text(
        "123 (python worker (test)) S "
        "1 2 3 4 5 6 7 8 9 10 11 12 13\n"
    )

    monkeypatch.setattr(cpu, "PROC_PATH", tmp_path)

    result = cpu.get_process_cpu_time(123)

    assert result == 23


def test_get_system_cpu_snapshot(tmp_path, monkeypatch):
    """Test reading aggregate CPU counters from /proc/stat."""

    stat_file = tmp_path / "stat"

    stat_file.write_text(
        "cpu 100 20 30 400 50 5 6 7\n"
        "cpu0 50 10 15 200 25 2 3 4\n"
    )

    monkeypatch.setattr(cpu, "PROC_PATH", tmp_path)

    total, idle = cpu.get_system_cpu_snapshot()

    assert total == 618
    assert idle == 450


def test_get_system_cpu_snapshot_missing_cpu_line(tmp_path, monkeypatch):
    """Test handling a stat file without aggregate CPU information."""

    stat_file = tmp_path / "stat"
    stat_file.write_text("intr 12345\n")

    monkeypatch.setattr(cpu, "PROC_PATH", tmp_path)

    import pytest

    with pytest.raises(RuntimeError):
        cpu.get_system_cpu_snapshot()


def test_get_cpu_snapshot(tmp_path, monkeypatch):
    """Test collecting system and process CPU counters."""

    (tmp_path / "123").mkdir()
    (tmp_path / "456").mkdir()
    (tmp_path / "self").mkdir()

    stat_file = tmp_path / "stat"
    stat_file.write_text("cpu 100 20 30 400 50 5 6 7\n")

    monkeypatch.setattr(cpu, "PROC_PATH", tmp_path)

    def fake_process_cpu_time(pid):
        if pid == 123:
            return 250

        if pid == 456:
            raise FileNotFoundError

        raise AssertionError("Unexpected PID")

    monkeypatch.setattr(
        cpu,
        "get_process_cpu_time",
        fake_process_cpu_time,
    )

    result = cpu.get_cpu_snapshot()

    assert result.system_total == 618
    assert result.system_idle == 450
    assert result.processes == {123: 250}


def test_measure_cpu_usage(monkeypatch):
    """Test measuring CPU usage between two snapshots."""

    previous = cpu.CpuSnapshot(
        system_total=1000,
        system_idle=800,
        processes={123: 100},
    )

    current = cpu.CpuSnapshot(
        system_total=1100,
        system_idle=850,
        processes={123: 120},
    )

    snapshots = iter([previous, current])

    monkeypatch.setattr(
        cpu,
        "get_cpu_snapshot",
        lambda: next(snapshots),
    )

    sleep_calls = []

    monkeypatch.setattr(
        cpu.time,
        "sleep",
        lambda interval: sleep_calls.append(interval),
    )

    result = cpu.measure_cpu_usage(interval=0.5)

    assert result == (50.0, {123: 20.0})
    assert sleep_calls == [0.5]

