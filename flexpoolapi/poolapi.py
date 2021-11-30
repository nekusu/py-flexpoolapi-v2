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

from typing import Dict, List
from datetime import datetime
from . import shared

__POOL_API_ENDPOINT__ = None


def update_endpoint(endpoint):
    global __POOL_API_ENDPOINT__
    __POOL_API_ENDPOINT__ = endpoint + "/pool"


class Hashrate:
    def __init__(self, regions: Dict, total: int):
        self.regions = regions
        self.total = total

    def __repr__(self):
        return "<flexpoolapi.pool.Hashrate object>"


class HashrateChartItem:
    def __init__(self, timestamp: int, regions: Dict, total: float):
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.regions = regions
        self.total = total

    def __repr__(self):
        return "<flexpoolapi.pool.HashrateChartItem object>"


class Coin:
    def __init__(
        self,
        ticker: str,
        name: str,
        decimal_places: int,
        share_difficulty: int,
        transaction_size: int,
        lowest_min_payout_threshold: int,
        difficulty_factor: int,
        hashrate_unit: str,
    ):
        self.ticker = ticker
        self.name = name
        self.decimal_places = decimal_places
        self.share_difficulty = share_difficulty
        self.transaction_size = transaction_size
        self.lowest_min_payout_threshold = lowest_min_payout_threshold
        self.difficulty_factor = difficulty_factor
        self.hashrate_unit = hashrate_unit

    def __repr__(self):
        return f"<flexpoolapi.pool.Coin object ({self.ticker})>"


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
        daily_reward_per_giga_hash_sec: int,
    ):
        self.reward = reward
        self.difficulty = difficulty
        self.hashrate = hashrate
        self.block_time = block_time
        self.daily_reward_per_giga_hash_sec = daily_reward_per_giga_hash_sec

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
        default_hashrate_si_prefix: str,
        applicable_hashrate_si_prefixes: List,
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
        self.default_hashrate_si_prefix = default_hashrate_si_prefix
        self.applicable_hashrate_si_prefixes = applicable_hashrate_si_prefixes
        self.decimal_places = decimal_places
        self.difficulty_factor = difficulty_factor
        self.website_link = website_link
        self.whitepaper_link = whitepaper_link
        self.chain_data = chain_data
        self.market_data = market_data

    def __repr__(self):
        return f"<flexpoolapi.pool.CoinFull object ({self.ticker})>"


class Miner:
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
        return f"<flexpoolapi.pool.Miner object ({self.address[:5 + 2] + '…' + self.address[-5:]})>"


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
        return f"<flexpoolapi.pool.HashrateDistribution object>"


class BlockStats:
    def __init__(self, blocks: int, uncles: int, orphans: int):
        self.blocks = blocks
        self.uncles = uncles
        self.orphans = orphans

    def __repr__(self):
        return f"<flexpoolapi.pool.BlockStats object>"


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


def coins() -> CoinsList:
    raw_data = shared.get(f"{__POOL_API_ENDPOINT__}/coins")
    classed_coins = []
    for coin in raw_data["coins"]:
        classed_coins.append(
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
    return CoinsList(classed_coins, raw_data["countervalues"])


def coins_full() -> List[CoinFull]:
    raw_coins = shared.get(f"{__POOL_API_ENDPOINT__}/coinsFull")
    classed_coins = []
    for coin in raw_coins:
        chain_data = coin["chainData"]
        market_data = coin["marketData"]
        classed_coins.append(
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
    return classed_coins


class PoolAPI:
    def __init__(self, coin: str):
        self.coin = coin
        self.params = [("coin", self.coin)]
        self.endpoint = __POOL_API_ENDPOINT__

    def hashrate(self) -> Hashrate:
        raw_data = shared.get(f"{self.endpoint}/hashrate", self.params)
        return Hashrate(raw_data["total"], raw_data["regions"])

    def average_hashrate(self) -> float:
        return shared.get(f"{self.endpoint}/averageHashrate", self.params)

    def hashrate_chart(self) -> List[HashrateChartItem]:
        raw_chart = shared.get(f"{self.endpoint}/hashrateChart", self.params)
        classed_chart = []
        for item in raw_chart:
            classed_chart.append(
                HashrateChartItem(item["timestamp"], item["regions"], item["total"])
            )
        return classed_chart

    def miner_count(self) -> int:
        return shared.get(f"{self.endpoint}/minerCount", self.params)

    def worker_count(self) -> int:
        return shared.get(f"{self.endpoint}/workerCount", self.params)

    def daily_reward_per_giga_hash_sec(self) -> int:
        return shared.get(f"{self.endpoint}/dailyRewardPerGigahashSec", self.params)

    def average_block_reward(self) -> int:
        return shared.get(f"{self.endpoint}/averageBlockReward", self.params)

    def average_luck(self) -> float:
        return shared.get(f"{self.endpoint}/averageLuck", self.params)

    def current_luck(self) -> float:
        return shared.get(f"{self.endpoint}/currentLuck", self.params)

    def network_hashrate(self) -> float:
        return shared.get(f"{self.endpoint}/networkHashrate", self.params)

    def network_difficulty(self) -> int:
        return shared.get(f"{self.endpoint}/networkDifficulty", self.params)

    def blocks(self, page: int = 0) -> shared.PageResponse:
        raw_page = shared.get(f"{self.endpoint}/blocks", self.params + [("page", page)])
        classed_blocks = []
        for block in raw_page["data"]:
            classed_blocks.append(
                shared.Block(
                    block["hash"],
                    block["number"],
                    block["type"],
                    block["miner"],
                    block["difficulty"],
                    block["timestamp"],
                    block["confirmed"],
                    block["roundTime"],
                    block["luck"],
                    block["region"],
                    block["staticBlockReward"],
                    block["txFeeReward"],
                    block["mevReward"],
                    block["reward"],
                )
            )
        return shared.PageResponse(
            classed_blocks, raw_page["totalItems"], raw_page["totalPages"]
        )

    def block_by_hash(self, block_hash: str) -> shared.Block:
        raw_block = shared.get(
            f"{self.endpoint}/blockByHash",
            self.params + [("blockHash", block_hash)],
        )
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

    def top_miners(self) -> List[Miner]:
        raw_miners = shared.get(f"{self.endpoint}/topMiners", self.params)
        classed_miners = []
        for miner in raw_miners:
            classed_miners.append(
                Miner(
                    miner["address"],
                    miner["hashrate"],
                    miner["workerCount"],
                    miner["firstJoined"],
                    miner["balance"],
                )
            )
        return classed_miners

    def blocks_chart(self) -> List[BlockChartItem]:
        raw_chart = shared.get(f"{self.endpoint}/blocksChart", self.params)
        classed_chart = []
        for item in raw_chart:
            classed_chart.append(
                BlockChartItem(
                    item["timestamp"],
                    item["rewards"],
                    item["blockCount"],
                    item["difficulty"],
                    item["luck"],
                )
            )
        return classed_chart

    def miners_distribution(self) -> List[HashrateDistribution]:
        raw_distribution = shared.get(
            f"{self.endpoint}/minersDistribution", self.params
        )
        classed_distribution = []
        for item in raw_distribution:
            classed_distribution.append(
                HashrateDistribution(item["hashrateLowerThan"], item["hashrate"])
            )
        return classed_distribution

    def block_statistics(self) -> BlockStatsResponse:
        raw_stats = shared.get(f"{self.endpoint}/blockStatistics", self.params)
        classed_stats = {}
        for item in raw_stats.keys():
            classed_stats[item] = BlockStats(
                raw_stats[item]["blocks"],
                raw_stats[item]["uncles"],
                raw_stats[item]["orphans"],
            )
        return BlockStatsResponse(
            classed_stats["daily"],
            classed_stats["weekly"],
            classed_stats["monthly"],
            classed_stats["total"],
        )
