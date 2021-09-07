# py-flexpoolapi-v2

Structured Python wrapper for Flexpool API v2.

# Installation

Install **py-flexpoolapi-v2**.

## Using pip
```sh
pip3 install flexpoolapi-v2
```

## Build from source
```sh
git clone https://github.com/nekusu/py-flexpoolapi-v2.git
cd py-flexpoolapi-v2
pip3 install -r requirements.txt
sudo make install  # or `sudo python3 setup.py install`
```

# Usage

Quick example:
```python
>>> import flexpoolapi
>>> from flexpoolapi.utils import *

# Coins
>>> coins = flexpoolapi.poolapi.coins()
>>> coins[0].name
'Ethereum'
>>> coins[1].name
'Chia'

# ETH Pool
>>> eth_pool = flexpoolapi.pool("eth")
>>> format_hashrate(eth_pool.hashrate().total, "eth")
'11.2 TH/s'
>>> eth_pool.miner_count()
20600
>>> eth_pool.worker_count()
50987

# XCH Pool
>>> xch_pool = flexpoolapi.pool("xch")
>>> format_hashrate(xch_pool.hashrate().total, "xch")
'207.9 PB'
>>> xch_pool.miner_count()
3530
>>> xch_pool.worker_count()
4933

# ETH Miner
>>> eth_miner = flexpoolapi.miner("eth", eth_pool.top_miners()[0].address)
>>> format_decimals(eth_miner.balance().balance, "eth")
'1.01524 ETH'
>>> format_hashrate(eth_miner.stats().current_effective_hashrate, "eth")
'1.6 TH/s'

# XCH Miner
>>> xch_miner = flexpoolapi.miner("xch", xch_pool.top_miners()[0].address)
>>> format_decimals(xch_miner.balance().balance, "xch")
'0.1692 XCH'
>>> format_hashrate(xch_miner.stats().current_effective_hashrate, "xch")
'2.3 PB'

# Locate Address
>>> flexpoolapi.minerapi.locate_address(eth_pool.top_miners()[0].address)
'eth'
```

For better understanding, I recommend reading the [Flexpool APIv2 documentation](https://www.flexpool.io/docs/api). All variables/functions names were renamed from camelCase (JavaScript) to snake_case (Python).

# License
MIT - Copyright (c) 2020 Flexpool
