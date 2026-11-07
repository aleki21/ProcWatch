from procwatch import system


def test_get_memory_info(tmp_path, monkeypatch):
    """Test reading memory information from a meminfo file."""

    proc_dir = tmp_path

    meminfo = proc_dir / "meminfo"
    meminfo.write_text(
        "MemTotal:       8000000 kB\n"
        "MemFree:        2000000 kB\n"
        "MemAvailable:   3000000 kB\n"
    )

    monkeypatch.setattr(system, "PROC_PATH", proc_dir)

    result = system.get_memory_info()

    assert result["MemTotal"] == 8000000
    assert result["MemFree"] == 2000000
    assert result["MemAvailable"] == 3000000


def test_get_memory_usage(tmp_path, monkeypatch):
    """Test calculating used memory and its percentage."""

    proc_dir = tmp_path

    meminfo = proc_dir / "meminfo"
    meminfo.write_text(
        "MemTotal:       8000000 kB\n"
        "MemAvailable:   3000000 kB\n"
    )

    monkeypatch.setattr(system, "PROC_PATH", proc_dir)

    used, total, percentage = system.get_memory_usage()

    assert used == 5000000
    assert total == 8000000
    assert percentage == 62.5


def test_get_load_average(tmp_path, monkeypatch):
    """Test reading the 1, 5 and 15 minute load averages."""

    proc_dir = tmp_path

    loadavg = proc_dir / "loadavg"
    loadavg.write_text("0.22 0.08 0.02 1/455 4223\n")

    monkeypatch.setattr(system, "PROC_PATH", proc_dir)

    result = system.get_load_average()

    assert result == (0.22, 0.08, 0.02)
