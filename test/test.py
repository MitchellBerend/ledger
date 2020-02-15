import sys
import unittest
sys.path.append("/api_caller")
from api_caller import api_caller_lib
import os


print(os.path.dirname(os.path.realpath(__file__)))


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



















if __name__ == "__main__":
    unittest.main()