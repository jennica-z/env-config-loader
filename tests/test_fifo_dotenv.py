import os
import pathlib
import sys
import threading

import pytest

from envloader import load_config_from_env_file

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="FIFOs are Unix-only")


def test_load_config_from_env_file_from_fifo(tmp_path: pathlib.Path, monkeypatch):
    fifo = tmp_path / ".env"
    os.mkfifo(fifo)  # create named pipe

    def writer():
        with open(fifo, "w", encoding="utf-8") as w:
            w.write("MY_PASSWORD=pipe-secret\n")

    t = threading.Thread(target=writer)
    t.start()

    # Ensure env is clean
    monkeypatch.delenv("MY_PASSWORD", raising=False)

    ok = load_config_from_env_file(dotenv_path=str(fifo), override=True)
    t.join(timeout=2)

    assert ok is True
    assert os.getenv("MY_PASSWORD") == "pipe-secret"
