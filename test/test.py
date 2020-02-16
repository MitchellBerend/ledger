import sys
import unittest
sys.path.append("/home/ledger/api_caller")
import random
import api_caller_lib

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
            {"timestamp": "2020-01-01","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-02","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-03","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-04","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-05","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-06","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"},
            {"timestamp": "2020-01-07","open": 80,"high": 80,"low": 80,"close": 80,"volume": 1000,"symbol": "MSFT"}]
        for _ in range(100):
            unordered.insert(random.choice(6),unordered.pop())
        self.assertEqual(api_caller_lib.format_data(),ordered)

















if __name__ == "__main__":
    unittest.main()