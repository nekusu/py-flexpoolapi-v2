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

import si_prefix

from flexpoolapi import poolapi
from . import exceptions


def format_hashrate(hashrate: int, coin: str):
    hashrate_unit = None
    for coin_ in poolapi.coins():
        if coin_.ticker == coin:
            hashrate_unit = coin_.hashrate_unit
    if not hashrate_unit:
        raise(exceptions.InvalidCoin(f"Coin {coin} is invalid!"))
    return si_prefix.si_format(hashrate) + hashrate_unit

def format_decimals(value: int, coin: str, prec=6):
    decimal_places = None
    for coin_ in poolapi.coins():
        if coin_.ticker == coin:
            decimal_places = coin_.decimal_places
    if not decimal_places:
        raise(exceptions.InvalidCoin(f"Coin {coin} is invalid!"))
    amount = round(value / 10 ** decimal_places, prec)
    if amount == int(amount):
        amount = int(amount)
    return f"{amount} {coin.upper()}"
