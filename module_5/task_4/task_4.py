import sys
import traceback
from io import IOBase


class Redirect:
    def __init__(self, stdout: IOBase = None, stderr: IOBase = None) -> None:
        self.stdout: IOBase = stdout
        self.stderr: IOBase = stderr
        self.old_stdout: IOBase = sys.stdout
        self.old_stderr: IOBase = sys.stderr

    def __enter__(self):
        if self.stdout is not None:
            sys.stdout = self.stdout
        if self.stderr is not None:
            sys.stderr = self.stderr

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool | None:
        if self.stdout is not None:
            sys.stdout.close()
            sys.stdout = self.old_stdout
        if self.stderr is not None:
            sys.stderr.write(traceback.format_exc())
            sys.stderr.close()
            sys.stderr = self.old_stderr

        return True
