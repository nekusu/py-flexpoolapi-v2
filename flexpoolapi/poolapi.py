#
#   Software distrubuted under MIT License (MIT)
#
#   Copyright (c) 2020 Flexpool
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import requests

from typing import Dict, List
from datetime import datetime
from . import shared

__POOL_API_ENDPOINT__ = None


def update_endpoint(endpoint):
    global __POOL_API_ENDPOINT__
    __POOL_API_ENDPOINT__ = endpoint + "/pool"


def coins():
    api_request = requests.get(f"{__POOL_API_ENDPOINT__}/coins")
    shared.check_response(api_request)
    api_request = api_request.json()["result"]
    coins_classed = []
    for coin in api_request["coins"]:
        coins_classed.append(
            Coin(
                coin["ticker"],
                coin["name"],
                coin["decimalPlaces"],
                coin["shareDifficulty"],
                coin["transactionSize"],
                coin["lowestMinPayoutThreshold"],
                coin["difficultyFactor"],
                coin["hashrateUnit"],
            )
        )
    return CoinsList(coins_classed, api_request["countervalues"])


def coins_full():
    api_request = requests.get(f"{__POOL_API_ENDPOINT__}/coinsFull")
    shared.check_response(api_request)
    coins_classed = []
    for coin in api_request.json()["result"]:
        chain_data = coin["chainData"]
        market_data = coin["marketData"]
        coins_classed.append(
            CoinFull(
                coin["ticker"],
                coin["name"],
                coin["algorithm"],
                coin["hashrateUnit"],
                coin["hashrate"],
                coin["minerCount"],
                coin["defaultHashrateSiPrefix"],
                coin["applicableHashrateSiPrefixes"],
                coin["decimalPlaces"],
                coin["difficultyFactor"],
                coin["websiteLink"],
                coin["whitepaperLink"],
                ChainData(
                    chain_data["reward"],
                    chain_data["difficulty"],
                    chain_data["hashrate"],
                    chain_data["blockTime"],
                    chain_data["dailyRewardPerGigaHashSec"],
                ),
                MarketData(
                    market_data["priceChange"],
                    market_data["prices"],
                    market_data["marketCaps"],
                ),
            )
        )
    return coins_classed


class Hashrate:
    def __init__(self, total: int, regions: Dict):
        self.regions = regions
        self.total = total

    def __repr__(self):
        servers = []
        for server_name, server_hashrate in self.regions.items():
            servers.append(f"{server_name} ({server_hashrate})")

        return "<flexpoolapi.pool.Hashrate object " + ", ".join(servers) + ">"


class HashrateChartItem:
    def __init__(self, timestamp: int, regions: Dict, total: float):
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.regions = regions
        self.total = total

    def __repr__(self):
        servers = []
        for server_name, server_hashrate in self.regions.items():
            servers.append(f"{server_name} ({server_hashrate})")

        return "<flexpoolapi.pool.HashrateChartItem object " + ", ".join(servers) + ">"


class Coin:
    def __init__(
        self,
        ticker: str,
        name: str,
        decimal_places: int,
        share_difficulty: int,
        transaction_size: int,
        min_payout_threshold: int,
        difficulty_factor: int,
        hashrate_unit: str,
    ):
        self.ticker = ticker
        self.name = name
        self.decimal_places = decimal_places
        self.share_difficulty = share_difficulty
        self.transaction_size = transaction_size
        self.lowest_min_payout_threshold = min_payout_threshold
        self.difficulty_factor = difficulty_factor
        self.hashrate_unit = hashrate_unit

    def __repr__(self):
        return f"<flexpoolapi.pool.Coin object {self.name} ({self.ticker})>"


class CoinsList:
    def __init__(self, coins: List, countervalues: List):
        self.coins = coins
        self.countervalues = countervalues

    def __getitem__(self, index):
        return self.coins[index]

    def __len__(self):
        return len(self.coins)

    def __repr__(self):
        return f"<flexpoolapi.shared.CoinsList object {str(self.coins)}>"

    def __str__(self):
        return str(self.coins)


class ChainData:
    def __init__(
        self,
        reward: int,
        difficulty: int,
        hashrate: float,
        block_time: float,
        daily_reward: int,
    ):
        self.reward = reward
        self.difficulty = difficulty
        self.hashrate = hashrate
        self.block_time = block_time
        self.daily_reward_per_giga_hash_sec = daily_reward

    def __repr__(self):
        return f"<flexpoolapi.pool.ChainData object>"


class MarketData:
    def __init__(self, price_change: float, prices: Dict, market_caps: Dict):
        self.price_change = price_change
        self.prices = prices
        self.market_caps = market_caps

    def __repr__(self):
        return f"<flexpoolapi.pool.MarketData object>"


class CoinFull:
    def __init__(
        self,
        ticker: str,
        name: str,
        algorithm: str,
        hashrate_unit: str,
        hashrate: float,
        miner_count: int,
        default_prefix: str,
        applicable_prefixes: List,
        decimal_places: int,
        difficulty_factor: int,
        website_link: str,
        whitepaper_link: str,
        chain_data: ChainData,
        market_data: MarketData,
    ):
        self.ticker = ticker
        self.name = name
        self.algorithm = algorithm
        self.hashrate_unit = hashrate_unit
        self.hashrate = hashrate
        self.miner_count = miner_count
        self.default_hashrate_si_prefix = default_prefix
        self.applicable_hashrate_si_prefixes = applicable_prefixes
        self.decimal_places = decimal_places
        self.difficulty_factor = difficulty_factor
        self.website_link = website_link
        self.whitepaper_link = whitepaper_link
        self.chain_data = chain_data
        self.market_data = market_data

    def __repr__(self):
        return f"<flexpoolapi.pool.CoinFull object {self.name} ({self.ticker})>"


class TopMiner:
    def __init__(
        self,
        address: str,
        hashrate: int,
        worker_count: int,
        first_joined: int,
        balance: int,
    ):
        self.address = address
        self.hashrate = hashrate
        self.worker_count = worker_count
        self.first_joined_time = datetime.fromtimestamp(first_joined)
        self.first_joined = first_joined
        self.balance = balance

    def __repr__(self):
        return f"<flexpoolapi.pool.TopMiner object {self.address}: {self.hashrate}>"


class BlockChartItem:
    def __init__(
        self,
        timestamp: int,
        rewards: int,
        block_count: int,
        difficulty: int,
        luck: float,
    ):
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.rewards = rewards
        self.block_count = block_count
        self.difficulty = difficulty
        self.luck = luck

    def __repr__(self):
        return f"<flexpoolapi.pool.BlockChartItem object>"


class HashrateDistribution:
    def __init__(self, lower_than: int, hashrate: int):
        self.hashrate_lower_than = lower_than
        self.hashrate = hashrate

    def __repr__(self):
        return f"<flexpoolapi.pool.HashrateDistribution object {self.hashrate_lower_than}: {self.hashrate}>"


class BlockStats:
    def __init__(self, blocks: int, uncles: int, orphans: int):
        self.blocks = blocks
        self.uncles = uncles
        self.orphans = orphans

    def __repr__(self):
        return f"<flexpoolapi.pool.BlockStats object {self.blocks} - {self.uncles} - {self.orphans}>"


class BlockStatsResponse:
    def __init__(
        self,
        daily: BlockStats,
        weekly: BlockStats,
        monthly: BlockStats,
        total: BlockStats,
    ):
        self.daily = daily
        self.weekly = weekly
        self.monthly = monthly
        self.total = total

    def __repr__(self):
        return f"<flexpoolapi.pool.BlockStatsResponse object>"


class PoolAPI:
    def __init__(self, coin: str):
        self.coin = coin
        self.params = [("coin", self.coin)]
        self.endpoint = __POOL_API_ENDPOINT__

    def hashrate(self):
        api_request = requests.get(f"{self.endpoint}/hashrate", params=self.params)
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        return Hashrate(api_request["total"], api_request["regions"])

    def average_hashrate(self):
        api_request = requests.get(
            f"{self.endpoint}/averageHashrate", params=self.params
        )
        shared.check_response(api_request)
        return api_request.json()["result"]

    def hashrate_chart(self):
        api_request = requests.get(f"{self.endpoint}/hashrateChart", params=self.params)
        shared.check_response(api_request)
        classed_hashrate_chart = []
        for item in api_request.json()["result"]:
            classed_hashrate_chart.append(
                HashrateChartItem(item["timestamp"], item["regions"], item["total"])
            )
        return classed_hashrate_chart

    def miner_count(self):
        api_request = requests.get(f"{self.endpoint}/minerCount", params=self.params)
        shared.check_response(api_request)
        return api_request.json()["result"]

    def worker_count(self):
        api_request = requests.get(f"{self.endpoint}/workerCount", params=self.params)
        shared.check_response(api_request)
        return api_request.json()["result"]

    def daily_reward_per_giga_hash_sec(self):
        api_request = requests.get(
            f"{self.endpoint}/dailyRewardPerGigahashSec", params=self.params
        )
        shared.check_response(api_request)
        return api_request.json()["result"]

    def average_block_reward(self):
        api_request = requests.get(
            f"{self.endpoint}/averageBlockReward", params=self.params
        )
        shared.check_response(api_request)
        return api_request.json()["result"]

    def average_luck(self):
        api_request = requests.get(f"{self.endpoint}/averageLuck", params=self.params)
        shared.check_response(api_request)
        return api_request.json()["result"]

    def current_luck(self):
        api_request = requests.get(f"{self.endpoint}/currentLuck", params=self.params)
        shared.check_response(api_request)
        return api_request.json()["result"]

    def network_hashrate(self):
        api_request = requests.get(
            f"{self.endpoint}/networkHashrate", params=self.params
        )
        shared.check_response(api_request)
        return api_request.json()["result"]

    def network_difficulty(self):
        api_request = requests.get(
            f"{self.endpoint}/networkDifficulty", params=self.params
        )
        shared.check_response(api_request)
        return api_request.json()["result"]

    def blocks(self, page: int = 0):
        api_request = requests.get(
            f"{self.endpoint}/blocks", params=self.params + [("page", page)]
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        classed_blocks = []
        for raw_block in api_request["data"]:
            classed_blocks.append(
                shared.Block(
                    raw_block["hash"],
                    raw_block["number"],
                    raw_block["type"],
                    raw_block["miner"],
                    raw_block["difficulty"],
                    raw_block["timestamp"],
                    raw_block["confirmed"],
                    raw_block["roundTime"],
                    raw_block["luck"],
                    raw_block["region"],
                    raw_block["staticBlockReward"],
                    raw_block["txFeeReward"],
                    raw_block["mevReward"],
                    raw_block["reward"],
                )
            )
        return shared.PageResponse(
            classed_blocks, api_request["totalItems"], api_request["totalPages"]
        )

    def block_by_hash(self, block_hash: str):
        api_request = requests.get(
            f"{self.endpoint}/blockByHash",
            params=self.params + [("blockHash", block_hash)],
        )
        shared.check_response(api_request)
        raw_block = api_request.json()["result"]
        return shared.Block(
            raw_block["hash"],
            raw_block["number"],
            raw_block["type"],
            raw_block["miner"],
            raw_block["difficulty"],
            raw_block["timestamp"],
            raw_block["confirmed"],
            raw_block["roundTime"],
            raw_block["luck"],
            raw_block["region"],
            raw_block["staticBlockReward"],
            raw_block["txFeeReward"],
            raw_block["mevReward"],
            raw_block["reward"],
        )

    def top_miners(self):
        api_request = requests.get(f"{self.endpoint}/topMiners", params=self.params)
        shared.check_response(api_request)
        classed_miners = []
        for miner in api_request.json()["result"]:
            classed_miners.append(
                TopMiner(
                    miner["address"],
                    miner["hashrate"],
                    miner["workerCount"],
                    miner["firstJoined"],
                    miner["balance"],
                )
            )
        return classed_miners

    def blocks_chart(self):
        api_request = requests.get(f"{self.endpoint}/blocksChart", params=self.params)
        shared.check_response(api_request)
        classed_blocks_chart = []
        for item in api_request.json()["result"]:
            classed_blocks_chart.append(
                BlockChartItem(
                    item["timestamp"],
                    item["rewards"],
                    item["blockCount"],
                    item["difficulty"],
                    item["luck"],
                )
            )
        return classed_blocks_chart

    def miners_distribution(self):
        api_request = requests.get(
            f"{self.endpoint}/minersDistribution", params=self.params
        )
        shared.check_response(api_request)
        classed_distribution = []
        for item in api_request.json()["result"]:
            classed_distribution.append(
                HashrateDistribution(item["hashrateLowerThan"], item["hashrate"])
            )
        return classed_distribution

    def block_statistics(self):
        api_request = requests.get(
            f"{self.endpoint}/blockStatistics", params=self.params
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        daily = api_request["daily"]
        weekly = api_request["weekly"]
        monthly = api_request["monthly"]
        total = api_request["total"]
        daily_stats = BlockStats(daily["blocks"], daily["uncles"], daily["orphans"])
        weekly_stats = BlockStats(weekly["blocks"], weekly["uncles"], daily["orphans"])
        monthly_stats = BlockStats(
            monthly["blocks"], monthly["uncles"], monthly["orphans"]
        )
        total_stats = BlockStats(total["blocks"], total["uncles"], total["orphans"])
        return BlockStatsResponse(daily_stats, weekly_stats, monthly_stats, total_stats)
