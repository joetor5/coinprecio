# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

import os
import argparse
import logging
from coinprecio import api
from influxdb_client_3 import InfluxDBClient3, Point

def main(args):
    
    coin_api_key = os.getenv("COINAPI_KEY")
    influx_token = os.getenv("INFLUXDB3_AUTH_TOKEN")

    coin_api = api(api_key=coin_api_key)
    influx_client = InfluxDBClient3(token=influx_token, 
                                    host=f"{args.host}:8181",
                                    database=args.db)
    
    coin_prices = coin_api.get_price_all()
    
    point = Point("prices")
    for coin in coin_prices:
        point.field(coin.lower(), coin_prices[coin])

    influx_client.write(point)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=str, default="coinprice")
    parser.add_argument("--host", type=str, default="localhost")

    args = parser.parse_args()
    
    main(args)
