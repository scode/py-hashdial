"""Implements a hash dial for hash based decision making.
"""
import hashlib
import math
import sys

from typing import TypeVar
from typing import List
from typing import Optional


# Maximum integer representable exactly as a float.
_MAX_FLOAT_REPRESENTABLE_INT = 2**(sys.float_info.mant_dig) - 1
_MIN_FLOAT_REPRESENTABLE_INT = -_MAX_FLOAT_REPRESENTABLE_INT


def _hfloat(b: bytes) -> float:
    h = hashlib.sha256()
    h.update(b)
    return float(int(h.hexdigest()[0:16], 16)) / 2**64


def is_selected(probability: float, b: bytes) -> bool:
    if probability < 0.0:
        raise ValueError('probability must be >= 0.0'.format(probability))
    if probability > 1.0:
        raise ValueError('probability must be <= 1.0'.format(probability))

    return _hfloat(b) < probability


def select_n(stop: int, b: bytes, *, start: Optional[int]=None) -> int:
    if start is None:
        start = 0

    if stop <= start:
        raise ValueError('stop ({}) must be > start ({})'.format(stop, start))

    if start < _MIN_FLOAT_REPRESENTABLE_INT or stop > _MAX_FLOAT_REPRESENTABLE_INT:
        raise ValueError('stop/start must be in range [{}, {}] due to limitations of floats',
                         _MIN_FLOAT_REPRESENTABLE_INT, _MAX_FLOAT_REPRESENTABLE_INT)

    return int(start + math.floor((stop - start) * _hfloat(b)))


BucketType = TypeVar('BucketType')


def select_bucket(buckets: List[BucketType], b: bytes) -> BucketType:
    return buckets[select_n(len(buckets), b)]
