# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from abc import ABC, abstractmethod
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .exceptions import *

_COIN_API_BACKEND = "coinmarketcap"
_COIN_API_CURRENCY = "USD"
_COIN_API_SYMBOL = "BTC"
_COIN_API_LIMIT = 100


class _CoinApi(ABC):

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_price_list(self):
        pass


class _CoinMarketCapApi(_CoinApi):
    def __init__(self, api_key: str, currency: str = _COIN_API_CURRENCY):
        self.api_key = api_key
        self.currency = currency
        self.api_domain = "https://pro-api.coinmarketcap.com"
        self.api_url_listings = self.api_domain + "/v1/cryptocurrency/listings/latest"
        self.api_url_quotes = self.api_domain + "/v2/cryptocurrency/quotes/latest"
        self.api_headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": api_key,
        }

        self.api_parameters_listings = {
            "limit": _COIN_API_LIMIT,
            "convert": self.currency
        }

        self.api_parameters_quotes = {
            "symbol": _COIN_API_SYMBOL,
            "convert": self.currency
        }

    def get_price(self, symbol: str = _COIN_API_SYMBOL):
        response = _fetch(self.api_url_quotes,
                          self.api_headers,
                          self.api_parameters_quotes).json()


        data = response["data"]
        timestamp = response["status"]["timestamp"]

        try:
            price = data[symbol][0]["quote"][self.currency]["price"]
        except KeyError as e:
            raise CoinApiParseError(f"Unable to parse price data: {e}") from None

        return {
            "timestamp": timestamp,
            symbol: price
        }

    def get_price_list(self, limit: int = None):
        price_list = {}
        if limit:
            self.api_parameters_listings["limit"] = limit

        response = _fetch(self.api_url_listings,
                          self.api_headers,
                          self.api_parameters_listings).json()

        data = response["data"]
        timestamp = response["status"]["timestamp"]

        for coin in data:
            try:
                symbol = coin["symbol"]
                price = coin["quote"][self.currency]["price"]
                price_list[symbol] = price
            except KeyError as e:
                raise CoinApiParseError(f"Unable to parse price data: {e}") from None

        return {
            "timestamp": timestamp,
            "coins": price_list
        }


def _fetch(api_url, api_headers, api_parameters):
    try:
        response = requests.get(api_url,
                                headers=api_headers,
                                params=api_parameters)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise CoinApiFetchError(f"Unable to connect to API URL: {api_url}") from None

    if response.status_code == 200:
        return response
    else:
        raise CoinApiFetchError(f"HTTP response was not 200 OK, got status: {response.status_code}")


def api(api_key: str, backend: str = _COIN_API_BACKEND, currency: str = _COIN_API_CURRENCY) -> _CoinApi:
    if backend == "coinmarketcap":
        return _CoinMarketCapApi(api_key, currency)
    else:
        raise CoinApiFactoryError(f"Unsupported API backend: {backend}")
