import http.server
import re
from collections import defaultdict
from typing import Any, Callable

T_handler_fun = Callable[["RequestRouter", re.Match], object]


class RequestRouter(http.server.BaseHTTPRequestHandler):
    # {"GET": {re.Pattern: fn}}
    all_handlers: dict[str, dict[re.Pattern, T_handler_fun]] = defaultdict(dict)

    def do_GET(self):
        self._dispatch_request(self.all_handlers["GET"])

    def do_POST(self):
        self._dispatch_request(self.all_handlers["POST"])

    def do_PATCH(self):
        self._dispatch_request(self.all_handlers["PATCH"])

    def do_DELETE(self):
        self._dispatch_request(self.all_handlers["DELETE"])

    def _dispatch_request(self, handlers):
        for pattern, handler in handlers.items():
            if match := pattern.fullmatch(self.path):
                return handler(self, match)
        self.send_error(500)

    @classmethod
    def register_handler(cls, method: str, pattern: str):
        def decorator(fun: T_handler_fun):
            cls.all_handlers[method.upper()][re.compile(pattern)] = fun
            return fun

        return decorator

    def get_body(self):
        if "Content-Length" not in self.headers:
            raise ValueError(
                "Request has no header Content-Length (Transfer-Encoding: chunked not implemented)"
            )
        return self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")

    def send_body(self, message: str, status: int = 200, headers: dict[str, Any] = {}):
        encoded = message.encode("utf-8")

        self.send_response(status)
        for hk, hv in headers.items():
            self.send_header(hk, hv)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Content-Type", "application/vnd.api+json")
        self.end_headers()
        self.wfile.write(encoded)
