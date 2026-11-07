import sys
import pytest

from procwatch import main


def test_parse_arguments_defaults(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["procwatch"])

    args = main.parse_arguments()

    assert args.sort == "cpu"
    assert args.limit == 20
    assert args.name is None
    assert args.interval == 2.0


def test_parse_arguments_custom_values(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "procwatch",
            "--sort", "memory",
            "--limit", "10",
            "--name", "chrome",
            "--interval", "1.5",
        ],
    )

    args = main.parse_arguments()

    assert args.sort == "memory"
    assert args.limit == 10
    assert args.name == "chrome"
    assert args.interval == 1.5


def test_parse_arguments_invalid_sort(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["procwatch", "--sort", "invalid"],
    )

    with pytest.raises(SystemExit):
        main.parse_arguments()

def test_main_calls_run_monitor(monkeypatch):
    captured = {}

    def mock_run_monitor(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "procwatch",
            "--sort", "memory",
            "--limit", "10",
            "--name", "chrome",
            "--interval", "1.5",
        ],
    )

    monkeypatch.setattr(main, "run_monitor", mock_run_monitor)

    main.main()

    assert captured == {
        "interval": 1.5,
        "sort_by": "memory",
        "limit": 10,
        "name": "chrome",
    }


def test_main_handles_keyboard_interrupt(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["procwatch"])

    def mock_run_monitor(**kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(main, "run_monitor", mock_run_monitor)

    main.main()

    captured = capsys.readouterr()

    assert "ProcWatch stopped." in captured.out