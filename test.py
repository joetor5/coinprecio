import unittest
import os
from coinprecio import api
from coinprecio.coinapi import _CoinApi

class TestCoinApi(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv("COINAPI_KEY")
        self.coin_api = api(api_key=self.api_key)
    
    def test_obj_init(self):
        self.assertIsInstance(self.coin_api, _CoinApi)
        self.assertIsNotNone(self.coin_api.api_key)

    def test_get_price(self):
        price = self.coin_api.get_price()
        self.assertIsInstance(price, float)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
