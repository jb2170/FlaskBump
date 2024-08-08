"""WSGI Bump"""

__version__ = "0.9.0"

import os
import json
import contextlib

from typing import Generator
from http import HTTPStatus

from .flocked import flocked

class App:
    def __init__(self, env, start_response) -> None:
        self.lock_filepath = os.environ.get(
            "WSGIBUMP_LOCK_FILEPATH",
            ".lock"
        )
        # keeping a separate lock file prevents headaches
        # from locking real files of interest

        self.state_filepath = os.environ.get(
            "WSGIBUMP_STATE_FILEPATH",
            "state.json"
        )

        self.env = env
        self.start_response = start_response

    @contextlib.contextmanager
    def locked(self):
        with open(self.lock_filepath, "ab") as lock_file:
            with flocked(lock_file):
                yield

    def read_config(self):
        with open(self.state_filepath, "r") as f:
            return json.load(f)

    def write_config(self, j):
        with open(self.state_filepath, "w") as f:
            json.dump(j, f)

    def __iter__(self):
        return self.do_200()

    def get_header(self, header_name: str) -> str | None:
        return self.env.get(f"HTTP_{header_name.replace('-', '_').upper()}")

    def do_respond(
        self,
        code: HTTPStatus,
        headers,
        body: bytes,
        content_type = "text/plain; charset=UTF-8"
    ) -> Generator[bytes, None, None]:
        response_line = f"{code} {code.phrase}"

        headers.append(("Content-Type", content_type))
        headers.append(("Content-Length", f"{len(body)}"))

        self.start_response(response_line, headers)

        yield body

    def do_200(self):
        with self.locked():
            j = self.read_config()
            count = j["count"]
            j["count"] += 1
            self.write_config(j)

        code = HTTPStatus.OK
        headers = []
        body = f"{count}\n".encode()

        return self.do_respond(code, headers, body)
