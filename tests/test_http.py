
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from app.app import OpsHubHandler


class HTTPApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), OpsHubHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_root_endpoint(self):
        with urlopen(f"{self.base_url}/") as response:
            body = json.load(response)

        self.assertEqual(response.status, 200)
        self.assertEqual(body["service"], "opshub")
        self.assertEqual(body["message"], "OpsHub is running")

    def test_health_endpoint(self):
        with urlopen(f"{self.base_url}/health") as response:
            body = json.load(response)

        self.assertEqual(response.status, 200)
        self.assertEqual(body["service"], "opshub")
        self.assertEqual(body["status"], "ok")

    def test_metrics_endpoint(self):
        with urlopen(f"{self.base_url}/metrics") as response:
            body = response.read().decode("utf-8")
            content_type = response.headers["Content-Type"]

        self.assertEqual(response.status, 200)
        self.assertTrue(
            content_type.startswith("text/plain; version=0.0.4")
        )
        self.assertIn("opshub_requests_total", body)
        self.assertIn("opshub_health_checks_total", body)
        self.assertIn("opshub_uptime_seconds", body)

    def test_unknown_endpoint_returns_not_found(self):
        try:
            urlopen(f"{self.base_url}/does-not-exist")
        except HTTPError as error:
            self.assertEqual(error.code, 404)
            error.close()
        else:
            self.fail("Expected a 404 HTTP error")


if __name__ == "__main__":
    unittest.main()
