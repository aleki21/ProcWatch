from dataclasses import dataclass


@dataclass
class Process:
    pid: int
    name: str
    state: str
    parent_pid: int
    memory_kb: int
    threads: int
    cpu_percent: float = 0.0