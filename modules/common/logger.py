from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Final


class Logger:
    # Minimal logger that writes to console and a per-run file.

    _LOGS_DIR: Final[str] = "logs"

    def __init__(self, name: str) -> None:
        self._name = name
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        self._run_dir = Path(self._LOGS_DIR) / timestamp
        self._run_dir.mkdir(parents=True, exist_ok=True)
        self._log_path = self._run_dir / f"{name}.log"

        # Create file immediately so tests can assert its existence
        self._log_path.touch(exist_ok=True)

    @property
    def log_dir(self) -> Path:
        """Directory containing this logger's outputs for the run."""

        return self._run_dir

    def _write(self, level: str, message: str) -> None:
        prefix = f"[{self._name}] {level.upper()}"
        line = f"{prefix}: {message}"

        # stdout for immediate feedback
        print(line)
        sys.stdout.flush()

        # append to the log file
        with self._log_path.open("a", encoding="utf-8") as fp:
            fp.write(line + os.linesep)

    def info(self, message: str) -> None:
        self._write("info", message)

    def warning(self, message: str) -> None:
        self._write("warning", message)

    def error(self, message: str) -> None:
        self._write("error", message)
