import sys
import unittest

sys.path.append("/home/mitchell/ledger/api_caller")
sys.path.append("/home/mitchell/ledger/track_handler")
import random
import api_caller_lib
import track_handler_lib


class test(unittest.TestCase):
    def test_retrieve_data(self):
        class mock_cur:
            def __init__(self):
                pass

            def execute(self, a):
                pass

            def fetchall(self):
                return [
                    ("1111-11-11", 100, 20, 50, 80, 100000, "MSFT", "random_hash")
                    for _ in range(100)
                ]

        class mock_con:
            def __init__(self, **_):
                self.cur = mock_cur()

            def cursor(self):
                return self.cur

            def close(self):
                pass

        api_caller_lib.sql.connect = mock_con
        api_caller_lib.sql.cursor = mock_cur
        self.assertEqual(
            api_caller_lib.retrieve_data("msft"),
            [
                ("1111-11-11", 100, 20, 50, 80, 100000, "MSFT", "random_hash")
                for _ in range(100)
            ],
        )



    def test_format_data(self):
        unordered = {    "Open":{        
        "2020-04-01T00:00:01.000Z":100,
        "2020-04-01T00:00:02.000Z":100,
        "2020-04-01T00:00:03.000Z":100,
        "2020-04-01T00:00:04.000Z":100,
        "2020-04-01T00:00:05.000Z":100},
    "High":{        
        "2020-04-01T00:00:01.000Z":100,
        "2020-04-01T00:00:02.000Z":100,
        "2020-04-01T00:00:03.000Z":100,
        "2020-04-01T00:00:04.000Z":100,
        "2020-04-01T00:00:05.000Z":100},
    "Low":{        
        "2020-04-01T00:00:01.000Z":100,
        "2020-04-01T00:00:02.000Z":100,
        "2020-04-01T00:00:03.000Z":100,
        "2020-04-01T00:00:04.000Z":100,
        "2020-04-01T00:00:05.000Z":100},
    "Close":{        
        "2020-04-01T00:00:01.000Z":100,
        "2020-04-01T00:00:02.000Z":100,
        "2020-04-01T00:00:03.000Z":100,
        "2020-04-01T00:00:04.000Z":100,
        "2020-04-01T00:00:05.000Z":100},
    "Volume":{        
        "2020-04-01T00:00:01.000Z":100,
        "2020-04-01T00:00:02.000Z":100,
        "2020-04-01T00:00:03.000Z":100,
        "2020-04-01T00:00:04.000Z":100,
        "2020-04-01T00:00:05.000Z":100}}
        ordered = [
            {
                "timestamp": "2020-01-05",
                "open": 100,
                "high": 100,
                "low": 100,
                "close": 100,
                "volume": 100,
                "symbol": "MSFT",
            },
            {
                "timestamp": "2020-01-04",
                "open": 100,
                "high": 100,
                "low": 100,
                "close": 100,
                "volume": 100,
                "symbol": "MSFT",
            },
            {
                "timestamp": "2020-01-03",
                "open": 100,
                "high": 100,
                "low": 100,
                "close": 100,
                "volume": 100,
                "symbol": "MSFT",
            },
            {
                "timestamp": "2020-01-02",
                "open": 100,
                "high": 100,
                "low": 100,
                "close": 100,
                "volume": 100,
                "symbol": "MSFT",
            },
            {
                "timestamp": "2020-01-01",
                "open": 100,
                "high": 100,
                "low": 100,
                "close": 100,
                "volume": 100,
                "symbol": "MSFT",
            },
        ]
        self.assertEqual(api_caller_lib.format_data("MSFT",unordered), ordered)

    def test_make_api_request(self):
        class mock_socket:
            def __init__(self, *args, **kwargs):
                self.data = """[{"close":100}]""".encode("utf-8")

            def connect(self, *args, **kwargs):
                pass

            def send(self, *args, **kwargs):
                pass

            def recv(self, *args, **kwargs):
                rv = self.data
                self.data = ""
                return rv

        def mock_gethostbyname(*args, **kwargs):
            return ""

        track_handler_lib.socket.gethostbyname = mock_gethostbyname
        track_handler_lib.socket.socket = mock_socket

        self.maxDiff = None
        self.assertEqual(track_handler_lib.make_api_request("test"), 100)

    def test_check_profile_for_existing_data(self):
        class mock_cur:
            def __init__(self):
                pass

            def execute(self, a):
                pass

            def fetchall(self):
                return []

        class mock_con:
            def __init__(self, **_):
                self.cur = mock_cur()

            def cursor(self):
                return self.cur

            def close(self):
                pass

        track_handler_lib.sql.connect = mock_con
        track_handler_lib.sql.cursor = mock_cur
        self.assertEqual(track_handler_lib.check_profile_for_existing_data(""), False)

    def test_get_value_from_api(self):
        class mock_socket:
            def __init__(self, *args, **kwargs):
                self.data = """[{
            "timestamp":"2020-02-14 16:00:00",
            "open":100.0,
            "high":100.0,
            "low":100.0,
            "close":100.0,
            "volume":20,
            "symbol":"NSRGY"
            }]""".encode(
                    "utf-8"
                )

            def connect(self, *args, **kwargs):
                pass

            def send(self, *args, **kwargs):
                pass

            def recv(self, *args, **kwargs):
                rv = self.data
                self.data = ""
                return rv

        def mock_gethostbyname(*args, **kwargs):
            return ""

        track_handler_lib.socket.gethostbyname = mock_gethostbyname
        track_handler_lib.socket.socket = mock_socket
        self.assertEqual(track_handler_lib.get_value_from_api(""), 100.0)


if __name__ == "__main__":
    unittest.main()
