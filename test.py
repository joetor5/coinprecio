# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

import unittest
import os
from coinprecio import api
from coinprecio.coinapi import _CoinApi, _CoinApiData
from coinprecio.exceptions import *
from coinprecio.symbols import symbols
from coinprecio.currencies import currencies


class TestCoinApi(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv("COINAPI_KEY")
        self.coin_api = api(api_key=self.api_key)
    
    def test_api_init(self):
        self.assertIsInstance(self.coin_api, _CoinApi)
        self.assertIsInstance(self.coin_api, _CoinApiData)

        attrs = [self.coin_api.api_key, self.coin_api.symbol, self.coin_api.currency]
        for attr in attrs:
            self.assertIsNotNone(attr)
            self.assertIsInstance(attr, str)
            self.assertNotEqual(len(attr), 0)

    def test_api_init_exceptions(self):
        for data in [1, ""]:
            with self.assertRaises(CoinApiDataError) as cm:
                capi = api(api_key=data)
            self.assertEqual(str(cm.exception), "api_key must be a string and not empty")

            with self.assertRaises(CoinApiDataError) as cm:
                capi = api(api_key=self.api_key, symbol=data)
            self.assertEqual(str(cm.exception), "symbol must be a string and in the supported symbol list")

            with self.assertRaises(CoinApiDataError) as cm:
                capi = api(api_key=self.api_key, currency=data)
            self.assertEqual(str(cm.exception), "currency must be a string and in the supported currency list")

    def test_get_price(self):
        price = self.coin_api.get_price()
        self.assertIsInstance(price, float)
        self.assertGreater(price, 0)

    def test_get_price_all(self):
        prices = self.coin_api.get_price_all()
        self.assertIsInstance(prices, dict)

        symbols_in_list = {symbol in symbols for symbol in prices.keys()}
        self.assertEqual(symbols_in_list, {True})

        prices_are_float = {isinstance(price, float) for price in prices.values()}
        self.assertEqual(prices_are_float, {True})

        prices_greater_than_zero = {price > 0 for price in prices.values()}
        self.assertEqual(prices_greater_than_zero, {True})

    def test_currencies(self):
        for currency in currencies:
            capi = api(api_key=self.api_key, currency=currency)
            price = capi.get_price()
            self.assertEqual(capi.currency, currency)
            self.assertIsInstance(price, float)
            self.assertGreater(price, 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
