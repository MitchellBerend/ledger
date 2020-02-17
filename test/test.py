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

            def execute(self,a):
                pass

            def fetchall(self):
                return [("1111-11-11",100,20,50,80,100000,"MSFT","random_hash") for _ in range(100)]

        class mock_con:
            def __init__(self,**_):
                self.cur = mock_cur()
            
            def cursor(self):
                return self.cur
            
            def close(self):
                pass

        api_caller_lib.sql.connect = mock_con
        api_caller_lib.sql.cursor = mock_cur
        self.assertEqual(api_caller_lib.retrieve_data("msft"),[("1111-11-11",100,20,50,80,100000,"MSFT","random_hash") for _ in range(100)])

    def test_format_data(self):
        unordered = [
            ("2020-01-01",80,80,80,80,1000,"MSFT"),
            ("2020-01-02",80,80,80,80,1000,"MSFT"),
            ("2020-01-03",80,80,80,80,1000,"MSFT"),
            ("2020-01-04",80,80,80,80,1000,"MSFT"),
            ("2020-01-05",80,80,80,80,1000,"MSFT"),
            ("2020-01-06",80,80,80,80,1000,"MSFT"),
            ("2020-01-07",80,80,80,80,1000,"MSFT")
        ]
        ordered = [
            {"timestamp": "2020-01-07","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-06","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-05","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-04","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-03","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-02","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-01","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"}]
        for _ in range(100):
            unordered.insert(random.choice([i for i in range(7)]),unordered.pop())
        self.assertEqual(api_caller_lib.format_data(unordered),ordered)

    def test_get_data_alphavantage(self):
        class mock_get:
            def __init__(self,*args,**kwargs):
                self.text = """{
                    "Meta Data": {
                    "1. Information": "Intraday (1min) open, high, low, close prices and volume",
                    "2. Symbol": "NSRGY",
                    "3. Last Refreshed": "2020-02-14 16:00:00",
                    "4. Interval": "1min",
                    "5. Output Size": "Compact",
                    "6. Time Zone": "US/Eastern"
                    },
                    "Time Series (1min)": {
                    "2020-02-14 16:00:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:59:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:58:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:57:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:56:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:55:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:53:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:52:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:51:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    },
                    "2020-02-14 15:49:00": {
                        "1. open": "100",
                        "2. high": "100",
                        "3. low": "100",
                        "4. close": "100",
                        "5. volume": "20"
                    }
                    }
                    }"""
        api_caller_lib.r.get = mock_get
        unordered = ""
        ordered = [{
            "timestamp":"2020-02-14 16:00:00",
            "open":100.0,
            "high":100.0,
            "low":100.0,
            "close":100.0,
            "volume":20,
            "symbol":"NSRGY"
            },
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:59:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:58:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:57:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:56:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:55:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:53:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:52:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:51:00",
            "volume":20},
            {"close":100.0,
            "high":100.0,
            "low":100.0,
            "open":100.0,
            "symbol":"NSRGY",
            "timestamp":"2020-02-14 15:49:00",
            "volume":20}
        ]
        self.maxDiff = None
        self.assertEqual(api_caller_lib.get_data_alphavantage("NSRGY",unordered),ordered)
    
    def test_make_api_request(self):
        class mock_socket:
            def __init__(self,*args,**kwargs):
                self.data = """[{"close":100}]"""

            def connect(self,*args,**kwargs):
                pass

            def send(self,*args,**kwargs):
                pass

            def recv(self, *args, **kwargs):
                rv = self.data
                self.data = ""
                return rv 
        track_handler_lib.socket.socket = mock_socket
        self.maxDiff = None
        self.assertEqual(track_handler_lib.make_api_request("test"),100)


    def test_check_profile_for_existing_data(self):
        pass

    def test_get_value_from_api(self):
        pass


if __name__ == "__main__":
    unittest.main()