import contextlib
import fcntl as fctl
from io import IOBase
from typing import Union

@contextlib.contextmanager
def flocked(f: Union[IOBase, int], op: int = fctl.LOCK_EX):
    if isinstance(f, IOBase):
        fd = f.fileno()
    else:
        fd = f

    try:
        fctl.flock(fd, op)
        yield
    finally:
        fctl.flock(fd, fctl.LOCK_UN)
