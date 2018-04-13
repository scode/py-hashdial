"""Implements a hash dial for hash based decision making.
"""
import hashlib

from typing import TypeVar
from typing import List


def _hfloat(b: bytes) -> float:
    h = hashlib.sha256()
    h.update(b)
    return float(int(h.hexdigest()[0:16], 16)) / 2**64


def is_selected(probability: float, b: bytes) -> bool:
    pass


def select_n(max_n: int, b: bytes) -> int:
    pass


BucketType = TypeVar('BucketType')


def select_bucket(buckets: List[BucketType], b: bytes) -> BucketType:
    pass
