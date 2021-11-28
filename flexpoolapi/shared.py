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

from typing import List
from datetime import datetime

from . import exceptions


class Block:
    def __init__(
        self,
        block_hash: str,
        number: int,
        block_type: str,
        miner: str,
        difficulty: int,
        timestamp: int,
        confirmed: bool,
        round_time: int,
        luck: float,
        region: str,
        static_block_reward: int,
        tx_fee_reward: int,
        mev_reward: int,
        reward: int,
    ):
        self.number = number
        self.hash = block_hash
        self.type = block_type
        self.miner = miner
        self.difficulty = difficulty
        self.time = datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp
        self.confirmed = confirmed
        self.round_time = round_time
        self.luck = luck
        self.region = region
        self.static_block_reward = static_block_reward
        self.tx_fee_reward = tx_fee_reward
        self.mev_reward = mev_reward
        self.reward = reward

    def __repr__(self):
        return (
            "<flexpoolapi.shared.Block object "
            f"{self.type.capitalize()} #{self.number} ({self.hash[:5 + 2] + '…' + self.hash[-5:]})>"
        )


class PageResponse:
    def __init__(self, contents: List, total_items: int, total_pages: int):
        self.contents = contents
        self.total_items = total_items
        self.total_pages = total_pages

    def __getitem__(self, index):
        return self.contents[index]

    def __len__(self):
        return len(self.contents)

    def __repr__(self):
        return f"<flexpoolapi.shared.PageResponse object {str(self.contents)}>"

    def __str__(self):
        return str(self.contents)


def check_response(request):
    if request.status_code not in [200, 201, 400]:
        raise (
            exceptions.UnexpectedStatusCode(
                f"API Returned unexpected status code: {request.status_code} "
                f"{request.reason} (Request URL: {request.url})"
            )
        )

    if request.text:
        error = (
            "error" in request.json()
            and request.json()["error"]
            or "message" in request.json()
            and request.json()["message"]
        )

        if error:
            raise (
                exceptions.APIError(
                    f"API Returned error: {error} (Request URL: {request.url})"
                )
            )
