# coinprecio

Crypto API client for fetching market price.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Install](#install)
- [Usage](#usage)
- [Supported API Backends](#supported-api-backends)
- [Supported Symbols](#supported-symbols)
- [Supported Currencies](#supported-currencies)
- [License](#license)

## <div id="prerequisites">Prerequisites</div>

Python >= 3.8

## <div id="install">Install</div>

```
TBA
```

## <div id="usage">Usage</div>

*api(api_key, backend="coinmarketcap", symbol="BTC", currency="USD")*

```
from coinprecio import api

api_key = "1234567890"

coinapi = api(api_key)
price = coinapi.get_price()
```

## <div id="supported-api-backends">Supported API Backends</div>

* coinmarketcap

## <div id="supported-symbols">Supported Symbols</div>

* BTC

## <div id="supported-currencies">Supported Currencies</div>

* USD

## <div id="license">License</div>

Distributed under the MIT License. See the accompanying file LICENSE.
