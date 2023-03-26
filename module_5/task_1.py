import subprocess
import os
import re
from flask import Flask


app = Flask(__name__)


def run_server(port: int) -> None:
    pids: [str] = _get_pids_for_port(port)
    _kill_all_processes(pids)
    app.run(port=port)


def _get_pids_for_port(port: int) -> [str]:
    list_open_files = subprocess.run(
        args=f"lsof -i :{port}",
        shell=True,
        capture_output=True,
        encoding='utf-8'
    )

    pids: [str] = re.findall(pattern=r"\s\d{4}\s", string=list_open_files.stdout)
    return pids


def _kill_all_processes(pids: [str]) -> None:
    for pid in pids:
        os.kill(int(pid), 9)


if __name__ == "__main__":
    run_server(6000)
