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

from datetime import datetime
from . import exceptions
from . import shared

__MINER_API_ENDPOINT__ = None


def update_endpoint(endpoint):
    global __MINER_API_ENDPOINT__
    __MINER_API_ENDPOINT__ = endpoint + "/miner"


def locate_address(address):
    api_request = requests.get(
        f"{__MINER_API_ENDPOINT__}/locateAddress", params=[("address", address)]
    )
    shared.check_response(api_request)
    coin = api_request.json()["result"]
    if not coin:
        raise (exceptions.MinerDoesNotExist(f"Miner {address} does not exist"))
    return coin


class NotificationPreferences:
    def __init__(self, workers_offline_notifications: bool, payout_notifications: bool):
        self.workers_offline_notifications = workers_offline_notifications
        self.payout_notifications = payout_notifications

    def __repr__(self):
        return f"<flexpoolapi.miner.NotificationPreferences object>"


class Notifications:
    def __init__(self, email: str):
        self.email = email

    def __repr__(self):
        return f"<flexpoolapi.miner.Notifications object {self.email}>"


class Details:
    def __init__(
        self,
        client_ip_address: str,
        current_fee_price: int,
        first_joined: int,
        ip_address: str,
        max_fee_price: int,
        payout_limit: int,
        network: str,
        notification_preferences: NotificationPreferences,
        notifications: Notifications,
    ):
        self.client_ip_address = client_ip_address
        self.current_network_fee_price = current_fee_price
        self.first_joined_time = datetime.fromtimestamp(first_joined)
        self.first_joined = first_joined
        self.ip_address = ip_address
        self.max_fee_price = max_fee_price
        self.payout_limit = payout_limit
        self.network = network
        self.notification_preferences = notification_preferences
        self.notifications = notifications

    def __repr__(self):
        return f"<flexpoolapi.miner.Details object {self.ip_address}>"


class Balance:
    def __init__(self, balance: int, balance_countervalue: float, price: float):
        self.balance = balance
        self.balance_countervalue = balance_countervalue
        self.price = price

    def __repr__(self):
        return f"<flexpoolapi.miner.Balance object {self.balance} ({self.balance_countervalue})>"


class WorkerCount:
    def __init__(self, online: int, offline: int):
        self.workers_online = online
        self.workers_offline = offline

    def __repr__(self):
        return f"<flexpoolapi.miner.WorkerCount object {self.workers_online}/{self.workers_offline}>"


class Stats:
    def __init__(
        self,
        effective: int,
        effective_day: int,
        reported: int,
        valid: int,
        stale: int,
        invalid: int,
    ):
        self.current_effective_hashrate = effective
        self.average_effective_hashrate = effective_day
        self.reported_hashrate = reported
        self.valid_shares = valid
        self.stale_shares = stale
        self.invalid_shares = invalid

    def __repr__(self):
        return f"<flexpoolapi.miner.Stats object {self.current_effective_hashrate}>"


class StatChartItem:
    def __init__(
        self,
        timestamp: int,
        effective: int,
        average_effective: int,
        reported: int,
        valid: int,
        stale: int,
        invalid: int,
    ):
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.effective_hashrate = effective
        self.average_effective_hashrate = average_effective
        self.reported_hashrate = reported
        self.valid_shares = valid
        self.stale_shares = stale
        self.invalid_shares = invalid

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
        reported: int,
        effective: int,
        average_effective: int,
        valid: int,
        stale: int,
        invalid: int,
        last_seen: int,
    ):
        self.name = name
        self.is_online = is_online
        self.count = count
        self.reported_hashrate = reported
        self.current_effective_hashrate = effective
        self.average_effective_hashrate = average_effective
        self.valid_shares = valid
        self.stale_shares = stale
        self.invalid_shares = invalid
        self.last_seen_time = datetime.fromtimestamp(last_seen)
        self.last_seen = last_seen

    def __repr__(self):
        return f"<flexpoolapi.worker.Worker object {self.name}>"


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
            f"{self.value} ({self.confirmed_time.strftime('%Y %b %d %H:%M')})>"
        )


class PaymentsStats:
    def __init__(
        self,
        value: int,
        fee: int,
        fee_percent: float,
        duration: int,
        paid: int,
        fees: int,
        count: int,
    ):
        self.average_value = value
        self.average_fee = fee
        self.average_fee_percent = fee_percent
        self.average_duration = duration
        self.total_paid = paid
        self.total_fees = fees
        self.transaction_count = count

    def __repr__(self):
        return (
            "<flexpoolapi.miner.PaymentsStats object "
            f"{self.average_value} ({self.transaction_count})>"
        )


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
        return f"<flexpoolapi.miner.BlockShare object {self.reward_share} ({self.round_share})>"


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
            f"{self.block_type.capitalize()} #{self.block_number} ({self.hash[:5 + 2] + '…' + self.hash[-5:]})>"
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
        api_request = requests.put(
            f"{self.endpoint}/payoutSettings",
            params=self.params
            + [
                ("ipAddress", ip_address),
                ("maxFeePrice", max_fee_price),
                ("payoutLimit", payout_limit),
                ("network", network),
            ],
        )
        shared.check_response(api_request)
        return True

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
        api_request = requests.put(
            f"{self.endpoint}/notificationSettings", params=self.params + params
        )
        shared.check_response(api_request)
        return True

    def details(self):
        api_request = requests.get(f"{self.endpoint}/details", params=self.params)
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        notification_preferences = api_request["notificationPreferences"]
        notifications = api_request["notifications"]
        return Details(
            api_request["clientIPAddress"],
            api_request["currentNetworkFeePrice"],
            api_request["firstJoined"],
            api_request["ipAddress"],
            api_request["maxFeePrice"],
            api_request["payoutLimit"],
            api_request["network"],
            NotificationPreferences(
                notification_preferences["workersOfflineNotifications"],
                notification_preferences["payoutNotifications"],
            ),
            Notifications(notifications["email"]),
        )

    def balance(self, countervalue: str = "USD"):
        api_request = requests.get(
            f"{self.endpoint}/balance",
            params=self.params + [("countervalue", countervalue)],
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        return Balance(
            api_request["balance"],
            api_request["balanceCountervalue"],
            api_request["price"],
        )

    def worker_count(self):
        api_request = requests.get(f"{self.endpoint}/workerCount", params=self.params)
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        return WorkerCount(api_request["workersOnline"], api_request["workersOffline"])

    def round_share(self):
        api_request = requests.get(f"{self.endpoint}/roundShare", params=self.params)
        shared.check_response(api_request)
        return api_request.json()["result"]

    def stats(self, worker_name: str = ""):
        api_request = requests.get(
            f"{self.endpoint}/stats", params=self.params + [("worker", worker_name)]
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        class_ = Stats(
            api_request["currentEffectiveHashrate"],
            api_request["averageEffectiveHashrate"],
            api_request["reportedHashrate"],
            api_request["validShares"],
            api_request["staleShares"],
            api_request["invalidShares"],
        )
        return class_

    def chart(self, worker_name: str = ""):
        api_request = requests.get(
            f"{self.endpoint}/chart", params=self.params + [("worker", worker_name)]
        )
        shared.check_response(api_request)
        items = []
        for item in api_request.json()["result"]:
            items.append(
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
        return items

    def workers(self):
        api_request = requests.get(f"{self.endpoint}/workers", params=self.params)
        shared.check_response(api_request)
        classed_workers = []
        for worker_ in api_request.json()["result"]:
            classed_workers.append(
                Worker(
                    worker_["name"],
                    worker_["isOnline"],
                    worker_["count"],
                    worker_["reportedHashrate"],
                    worker_["currentEffectiveHashrate"],
                    worker_["averageEffectiveHashrate"],
                    worker_["validShares"],
                    worker_["staleShares"],
                    worker_["invalidShares"],
                    worker_["lastSeen"],
                )
            )
        return classed_workers

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

    def payments(self, countervalue: str = "USD", page: int = 0):
        api_request = requests.get(
            f"{self.endpoint}/payments",
            params=self.params + [("countervalue", countervalue), ("page", page)],
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        classed_payments = []
        if api_request["data"]:
            for raw_tx in api_request["data"]:
                classed_payments.append(
                    Payment(
                        raw_tx["hash"],
                        raw_tx["timestamp"],
                        raw_tx["value"],
                        raw_tx["fee"],
                        raw_tx["feePercent"],
                        raw_tx["feePrice"],
                        raw_tx["duration"],
                        raw_tx["confirmed"],
                        raw_tx["confirmedTimestamp"],
                        raw_tx["network"],
                    )
                )
        return shared.PageResponse(
            classed_payments, api_request["totalItems"], api_request["totalPages"]
        )

    def payments_stats(self, countervalue: str = "USD"):
        api_request = requests.get(
            f"{self.endpoint}/paymentsStats",
            params=self.params + [("countervalue", countervalue)],
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        raw_tx = api_request["lastPayment"]
        stats = api_request["stats"]
        return PaymentsStatsResponse(
            api_request["countervalue"],
            Payment(
                raw_tx["hash"],
                raw_tx["timestamp"],
                raw_tx["value"],
                raw_tx["fee"],
                raw_tx["feePercent"],
                raw_tx["feePrice"],
                raw_tx["duration"],
                raw_tx["confirmed"],
                raw_tx["confirmedTimestamp"],
                raw_tx["network"],
            ),
            PaymentsStats(
                stats["averageValue"],
                stats["averageFee"],
                stats["averageFeePercent"],
                stats["averageDuration"],
                stats["totalPaid"],
                stats["totalFees"],
                stats["transactionCount"],
            ),
        )

    def round_share_at(self, block_hash: str):
        api_request = requests.get(
            f"{self.endpoint}/roundShareAt",
            params=self.params + [("blockHash", block_hash)],
        )
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        return BlockShare(api_request["rewardShare"], api_request["roundShare"])

    def block_rewards(self):
        api_request = requests.get(f"{self.endpoint}/blockRewards", params=self.params)
        shared.check_response(api_request)
        api_request = api_request.json()["result"]
        classed_rewards = []
        for raw_data in api_request:
            classed_rewards.append(
                BlockRewards(
                    raw_data["share"],
                    raw_data["reward"],
                    raw_data["confirmed"],
                    raw_data["hash"],
                    raw_data["timestamp"],
                    raw_data["blockNumber"],
                    raw_data["blockType"],
                )
            )
        return classed_rewards
