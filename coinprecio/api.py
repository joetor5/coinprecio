# Copyright (c) 2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

from abc import ABC, abstractmethod
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .exceptions import *

# defaults
_COIN_API_BACKEND = "coinmarketcap"
_COIN_API_CURRENCY = "USD"

class _CoinApi(ABC):

    @abstractmethod
    def get_price(self):
        pass

    def fetch(self, api_url, api_headers, api_parameters):
        try:
            response = requests.get(api_url,
                                    headers=api_headers,
                                    params=api_parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise CoinApiFetchError("Unable to connect to API URL") from None

        if response.status_code == 200:
            return response
        else:
            raise CoinApiFetchError("HTTP response was not 200 OK, got status: {}".format(response.status_code))


class _CoinMarketCapApi(_CoinApi):
    def __init__(self, api_key: str, currency: str = "USD"):
        self.api_key = api_key
        self.currency = currency
        self.api_endpoint = "/v1/cryptocurrency/listings/latest"
        self.api_url = "https://pro-api.coinmarketcap.com" + self.api_endpoint
        self.api_header = "X-CMC_PRO_API_KEY"
        self.api_headers = {
            "Accepts": "application/json",
            self.api_header: api_key,
        }

        self.api_parameters = {
            "start": "1",
            "limit": "1",
            "convert": self.currency
        }


    def get_price(self, coin: str = None):
        response = self.fetch(self.api_url,
                              self.api_headers,
                              self.api_parameters)

        data = response.json()
        try:
            coin_price = data["data"][0]["quote"][self.currency]["price"]
        except KeyError:
            raise CoinApiParseError("Unable to parse price data from") from None

        return round(coin_price, 2)


class CoinApiFactory:
    @staticmethod
    def create(api_key: str, backend: str = _COIN_API_BACKEND, currency: str = _COIN_API_CURRENCY):
        if backend == "coinmarketcap":
            return _CoinMarketCapApi(api_key, currency)
        else:
            raise CoinApiFactoryError("Unsupported API backend:", backend)

