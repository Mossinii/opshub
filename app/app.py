import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


APP_NAME = os.getenv("APP_NAME", "opshub")
APP_ENV = os.getenv("APP_ENV", "development")


def build_health_response():
    return {
        "service": APP_NAME,
        "status": "ok",
        "environment": APP_ENV,
    }


class OpsHubHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_json(
                200,
                {
                    "service": APP_NAME,
                    "message": "OpsHub is running",
                },
            )
        elif self.path == "/health":
            self.send_json(200, build_health_response())
        else:
            self.send_json(
                404,
                {
                    "error": "not_found",
                },
            )

    def log_message(self, format_string, *args):
        print(f"[http] {self.address_string()} - {format_string % args}")


def run():
    port = int(os.getenv("APP_PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), OpsHubHandler)

    print(f"{APP_NAME} listening on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
