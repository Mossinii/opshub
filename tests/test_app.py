import unittest

from app.app import build_health_response


class HealthResponseTests(unittest.TestCase):
    def test_health_response_is_healthy(self):
        response = build_health_response()

        self.assertEqual(response["service"], "opshub")
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["environment"], "development")


if __name__ == "__main__":
    unittest.main()
