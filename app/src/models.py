#
#   Written by Pavel Kononov from LightningBounties.com
#   For MIT Bitcoin Hackathon 2025
#
#   Happy hacking!
#

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Account:
    id: str
    user: str
    name: str
    adminkey: str
    inkey: str
    deleted: bool
    currency: str
    balance_msat: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    extra: dict | None = None


@dataclass
class Wallet:
    id: str
    user: str
    name: str
    adminkey: str
    inkey: str
    deleted: bool
    currency: str
    balance_msat: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    extra: dict | None = None


@dataclass
class WalletInfo:
    name: str
    balance: int


@dataclass
class Invoice:
    checking_id: str
    payment_hash: str
    wallet_id: str
    amount: int
    fee: int
    bolt11: str
    status: str
    memo: str
    expiry: datetime
    webhook: str
    webhook_status: int
    preimage: str
    tag: str
    extension: str
    time: datetime
    created_at: datetime
    updated_at: datetime
    extra: dict
    payment_request: str
    lnurl_response: Any | None = None

    def __post_init__(self):
        # If payment_request is not provided, use bolt11
        if self.payment_request is None:
            self.payment_request = self.bolt11

# Schema from feb18 lnbits
# {
#   "checking_id": "string",
#   "payment_hash": "string",
#   "wallet_id": "string",
#   "amount": 0,
#   "fee": 0,
#   "bolt11": "string",
#   "status": "pending",
#   "memo": "string",
#   "expiry": "2025-04-04T19:49:27.858Z",
#   "webhook": "string",
#   "webhook_status": 0,
#   "preimage": "string",
#   "tag": "string",
#   "extension": "string",
#   "time": "2025-04-04T19:49:27.858Z",
#   "created_at": "2025-04-04T19:49:27.858Z",
#   "updated_at": "2025-04-04T19:49:27.858Z",
#   "extra": {}
# }