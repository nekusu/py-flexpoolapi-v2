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

from typing import List, Union
from datetime import datetime
from . import exceptions
from . import shared

__MINER_API_ENDPOINT__ = None


def update_endpoint(endpoint):
    global __MINER_API_ENDPOINT__
    __MINER_API_ENDPOINT__ = endpoint + "/miner"


def locate_address(address) -> str:
    coin = shared.get(f"{__MINER_API_ENDPOINT__}/locateAddress", [("address", address)])
    if not coin:
        raise (exceptions.MinerDoesNotExist(f"Miner {address} does not exist"))
    return coin


class NotificationPreferences:
    def __init__(self, workers_offline_notifications: bool, payout_notifications: bool):
        self.workers_offline_notifications = workers_offline_notifications
        self.payout_notifications = payout_notifications

    def __repr__(self):
        return "<flexpoolapi.miner.NotificationPreferences object>"


class Notifications:
    def __init__(self, email: str):
        self.email = email

    def __repr__(self):
        return "<flexpoolapi.miner.Notifications object>"


class Details:
    def __init__(
        self,
        client_ip_address: str,
        current_network_fee_price: int,
        first_joined: int,
        ip_address: str,
        max_fee_price: int,
        payout_limit: int,
        network: str,
        notification_preferences: NotificationPreferences,
        notifications: Notifications,
    ):
        self.client_ip_address = client_ip_address
        self.current_network_fee_price = current_network_fee_price
        self.first_joined_time = datetime.fromtimestamp(first_joined)
        self.first_joined = first_joined
        self.ip_address = ip_address
        self.max_fee_price = max_fee_price
        self.payout_limit = payout_limit
        self.network = network
        self.notification_preferences = notification_preferences
        self.notifications = notifications

    def __repr__(self):
        return f"<flexpoolapi.miner.Details object (IP: {self.ip_address})>"


class Balance:
    def __init__(self, balance: int, balance_countervalue: float, price: float):
        self.balance = balance
        self.balance_countervalue = balance_countervalue
        self.price = price

    def __repr__(self):
        return f"<flexpoolapi.miner.Balance object>"


class WorkerCount:
    def __init__(self, workers_online: int, workers_offline: int):
        self.workers_online = workers_online
        self.workers_offline = workers_offline

    def __repr__(self):
        return (
            "<flexpoolapi.miner.WorkerCount object "
            f"(Online: {self.workers_online} / Offline: {self.workers_offline})>"
        )


class Stats:
    def __init__(
        self,
        current_effective_hashrate: Union[int, float],
        average_effective_hashrate: Union[int, float],
        reported_hashrate: Union[int, float],
        valid_shares: int,
        stale_shares: int,
        invalid_shares: int,
    ):
        self.current_effective_hashrate = current_effective_hashrate
        self.average_effective_hashrate = average_effective_hashrate
        self.reported_hashrate = reported_hashrate
        self.valid_shares = valid_shares
        self.stale_shares = stale_shares
        self.invalid_shares = invalid_shares

    def __repr__(self):
        return "<flexpoolapi.miner.Stats object>"


class StatChartItem:
    def __init__(
        self,
        timestamp: int,
        effective_hashrate: Union[int, float],
        average_effective_hashrate: Union[int, float],
        reported_hashrate: Union[int, float],
        valid_shares: int,
        stale_shares: int,
        invalid_shares: int,
    ):
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.effective_hashrate = effective_hashrate
        self.average_effective_hashrate = average_effective_hashrate
        self.reported_hashrate = reported_hashrate
        self.valid_shares = valid_shares
        self.stale_shares = stale_shares
        self.invalid_shares = invalid_shares

    def __repr__(self):
        return (
            "<flexpoolapi.miner.StatChartItem object "
            f"({self.time.strftime('%Y %b %d %H:%M')})>"
        )


class Worker:
    def __init__(
        self,
        name: str,
        is_online: bool,
        count: int,
        reported_hashrate: Union[int, float],
        current_effective_hashrate: Union[int, float],
        average_effective_hashrate: Union[int, float],
        valid_shares: int,
        stale_shares: int,
        invalid_shares: int,
        last_seen: int,
    ):
        self.name = name
        self.is_online = is_online
        self.count = count
        self.reported_hashrate = reported_hashrate
        self.current_effective_hashrate = current_effective_hashrate
        self.average_effective_hashrate = average_effective_hashrate
        self.valid_shares = valid_shares
        self.stale_shares = stale_shares
        self.invalid_shares = invalid_shares
        self.last_seen_time = datetime.fromtimestamp(last_seen)
        self.last_seen = last_seen

    def __repr__(self):
        return f"<flexpoolapi.miner.Worker object ({self.name})>"


class Payment:
    def __init__(
        self,
        tx_hash: str,
        timestamp: int,
        value: int,
        fee: int,
        fee_percent: float,
        fee_price: int,
        duration: int,
        confirmed: bool,
        confirmed_timestamp: int,
        network: str,
    ):
        self.hash = tx_hash
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.value = value
        self.fee = fee
        self.fee_percent = fee_percent
        self.fee_price = fee_price
        self.duration = duration
        self.confirmed = confirmed
        self.confirmed_time = datetime.fromtimestamp(confirmed_timestamp)
        self.confirmed_timestamp = confirmed_timestamp
        self.network = network

    def __repr__(self):
        return (
            "<flexpoolapi.miner.Payment object "
            f"({self.confirmed_time.strftime('%Y %b %d %H:%M')})>"
        )


class PaymentsStats:
    def __init__(
        self,
        average_value: int,
        average_fee: int,
        average_fee_percent: float,
        average_duration: int,
        total_paid: int,
        total_fees: int,
        transaction_count: int,
    ):
        self.average_value = average_value
        self.average_fee = average_fee
        self.average_fee_percent = average_fee_percent
        self.average_duration = average_duration
        self.total_paid = total_paid
        self.total_fees = total_fees
        self.transaction_count = transaction_count

    def __repr__(self):
        return "<flexpoolapi.miner.PaymentsStats object>"


class PaymentsStatsResponse:
    def __init__(
        self, countervalue: float, last_payment: Payment, stats: PaymentsStats
    ):
        self.countervalue = countervalue
        self.last_payment = last_payment
        self.stats = stats

    def __repr__(self):
        return "<flexpoolapi.miner.PaymentsStatsResponse object>"


class BlockShare:
    def __init__(self, reward_share: float, round_share: float):
        self.reward_share = reward_share
        self.round_share = round_share

    def __repr__(self):
        return "<flexpoolapi.miner.BlockShare object>"


class BlockRewards:
    def __init__(
        self,
        share: float,
        reward: float,
        confirmed: bool,
        block_hash: str,
        timestamp: int,
        block_number: int,
        block_type: str,
    ):
        self.share = share
        self.reward = reward
        self.confirmed = confirmed
        self.hash = block_hash
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.block_number = block_number
        self.block_type = block_type

    def __repr__(self):
        return (
            "<flexpoolapi.miner.BlockRewards object "
            f"({self.block_type.capitalize()} #{self.block_number})>"
        )


class MinerAPI:
    def __init__(self, coin: str, address: str):
        coin = coin.lower()
        self.coin = coin
        self.address = address
        self.params = [("coin", self.coin), ("address", self.address)]
        self.endpoint = __MINER_API_ENDPOINT__
        locate_address(address)

    def payout_settings(
        self, ip_address: str, max_fee_price: int, payout_limit: int, network: str
    ):
        shared.post(
            f"{self.endpoint}/payoutSettings",
            self.params
            + [
                ("ipAddress", ip_address),
                ("maxFeePrice", max_fee_price),
                ("payoutLimit", payout_limit),
                ("network", network),
            ],
        )

    def notification_settings(
        self,
        ip_address: str,
        email_enabled: bool,
        email: str = None,
        payment_notifications: bool = None,
        workers_offline_notifications: bool = None,
    ):
        params = [("ipAddress", ip_address), ("emailEnabled", email_enabled)]
        if email_enabled:
            params += [
                ("email", email),
                ("paymentNotifications", payment_notifications),
                ("workersOfflineNotifications", workers_offline_notifications),
            ]
        shared.post(f"{self.endpoint}/notificationSettings", self.params + params)

    def details(self) -> Details:
        raw_details = shared.get(f"{self.endpoint}/details", self.params)
        preferences = raw_details["notificationPreferences"]
        notifications = raw_details["notifications"]
        return Details(
            raw_details["clientIPAddress"],
            raw_details["currentNetworkFeePrice"],
            raw_details["firstJoined"],
            raw_details["ipAddress"],
            raw_details["maxFeePrice"],
            raw_details["payoutLimit"],
            raw_details["network"],
            NotificationPreferences(
                preferences["workersOfflineNotifications"],
                preferences["payoutNotifications"],
            )
            if preferences
            else None,
            Notifications(notifications["email"]) if notifications else None,
        )

    def balance(self, countervalue: str = "") -> Balance:
        raw_data = shared.get(
            f"{self.endpoint}/balance",
            self.params + [("countervalue", countervalue)],
        )
        return Balance(
            raw_data["balance"],
            raw_data["balanceCountervalue"],
            raw_data["price"],
        )

    def worker_count(self) -> WorkerCount:
        raw_count = shared.get(f"{self.endpoint}/workerCount", self.params)
        return WorkerCount(raw_count["workersOnline"], raw_count["workersOffline"])

    def round_share(self) -> float:
        return shared.get(f"{self.endpoint}/roundShare", self.params)

    def stats(self, worker_name: str = "") -> Stats:
        raw_stats = shared.get(
            f"{self.endpoint}/stats", self.params + [("worker", worker_name)]
        )
        return Stats(
            raw_stats["currentEffectiveHashrate"],
            raw_stats["averageEffectiveHashrate"],
            raw_stats["reportedHashrate"],
            raw_stats["validShares"],
            raw_stats["staleShares"],
            raw_stats["invalidShares"],
        )

    def chart(self, worker_name: str = "") -> List[StatChartItem]:
        raw_chart = shared.get(
            f"{self.endpoint}/chart", self.params + [("worker", worker_name)]
        )
        classed_items = []
        for item in raw_chart:
            classed_items.append(
                StatChartItem(
                    item["timestamp"],
                    item["effectiveHashrate"],
                    item["averageEffectiveHashrate"],
                    item["reportedHashrate"],
                    item["validShares"],
                    item["staleShares"],
                    item["invalidShares"],
                )
            )
        return classed_items

    def workers(self) -> List[Worker]:
        raw_workers = shared.get(f"{self.endpoint}/workers", self.params)
        classed_workers = []
        for worker in raw_workers:
            classed_workers.append(
                Worker(
                    worker["name"],
                    worker["isOnline"],
                    worker["count"],
                    worker["reportedHashrate"],
                    worker["currentEffectiveHashrate"],
                    worker["averageEffectiveHashrate"],
                    worker["validShares"],
                    worker["staleShares"],
                    worker["invalidShares"],
                    worker["lastSeen"],
                )
            )
        return classed_workers

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

    def payments(self, countervalue: str = "", page: int = 0) -> shared.PageResponse:
        raw_page = shared.get(
            f"{self.endpoint}/payments",
            self.params + [("countervalue", countervalue), ("page", page)],
        )
        classed_payments = []
        for payment in raw_page["data"]:
            classed_payments.append(
                Payment(
                    payment["hash"],
                    payment["timestamp"],
                    payment["value"],
                    payment["fee"],
                    payment["feePercent"],
                    payment["feePrice"],
                    payment["duration"],
                    payment["confirmed"],
                    payment["confirmedTimestamp"],
                    payment["network"],
                )
            )
        return shared.PageResponse(
            classed_payments, raw_page["totalItems"], raw_page["totalPages"]
        )

    def payments_stats(self, countervalue: str = "") -> PaymentsStatsResponse:
        raw_data = shared.get(
            f"{self.endpoint}/paymentsStats",
            self.params + [("countervalue", countervalue)],
        )
        payment = raw_data["lastPayment"]
        stats = raw_data["stats"]
        return PaymentsStatsResponse(
            raw_data["countervalue"],
            Payment(
                payment["hash"],
                payment["timestamp"],
                payment["value"],
                payment["fee"],
                payment["feePercent"],
                payment["feePrice"],
                payment["duration"],
                payment["confirmed"],
                payment["confirmedTimestamp"],
                payment["network"],
            )
            if payment
            else None,
            PaymentsStats(
                stats["averageValue"],
                stats["averageFee"],
                stats["averageFeePercent"],
                stats["averageDuration"],
                stats["totalPaid"],
                stats["totalFees"],
                stats["transactionCount"],
            )
            if stats
            else None,
        )

    def round_share_at(self, block_hash: str) -> BlockShare:
        raw_data = shared.get(
            f"{self.endpoint}/roundShareAt",
            self.params + [("blockHash", block_hash)],
        )
        return BlockShare(raw_data["rewardShare"], raw_data["roundShare"])

    def block_rewards(self) -> List[BlockRewards]:
        raw_rewards = shared.get(f"{self.endpoint}/blockRewards", self.params)
        classed_rewards = []
        for reward in raw_rewards:
            classed_rewards.append(
                BlockRewards(
                    reward["share"],
                    reward["reward"],
                    reward["confirmed"],
                    reward["hash"],
                    reward["timestamp"],
                    reward["blockNumber"],
                    reward["blockType"],
                )
            )
        return classed_rewards
