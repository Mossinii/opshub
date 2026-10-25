import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


APP_NAME = os.getenv("APP_NAME", "opshub")
APP_ENV = os.getenv("APP_ENV", "development")

metrics_lock = threading.Lock()
request_count = 0
health_check_count = 0
started_at = time.time()


def build_health_response():
    return {
        "service": APP_NAME,
        "status": "ok",
        "environment": APP_ENV,
    }


def build_metrics_response():
    uptime_seconds = time.time() - started_at

    with metrics_lock:
        current_request_count = request_count
        current_health_check_count = health_check_count

    return (
        "# HELP opshub_requests_total Total number of HTTP requests received.\n"
        "# TYPE opshub_requests_total counter\n"
        f"opshub_requests_total {current_request_count}\n"
        "# HELP opshub_health_checks_total Total number of health checks received.\n"
        "# TYPE opshub_health_checks_total counter\n"
        f"opshub_health_checks_total {current_health_check_count}\n"
        "# HELP opshub_uptime_seconds Time since the application started.\n"
        "# TYPE opshub_uptime_seconds gauge\n"
        f"opshub_uptime_seconds {uptime_seconds:.2f}\n"
    )


class OpsHubHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_metrics(self):
        body = build_metrics_response().encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global request_count, health_check_count

        with metrics_lock:
            request_count += 1

        if self.path == "/":
            self.send_json(
                200,
                {
                    "service": APP_NAME,
                    "message": "OpsHub is running",
                },
            )
        elif self.path == "/health":
            with metrics_lock:
                health_check_count += 1

            self.send_json(200, build_health_response())
        elif self.path == "/metrics":
            self.send_metrics()
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
