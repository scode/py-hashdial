"""Implements a hash dial for hash based decision making.
"""
import hashlib
import math
import sys

from typing import TypeVar
from typing import Optional
from typing import Sequence

DEFAULT_SEED = b''

_MAX_FLOAT_REPRESENTABLE_INT = 2**(sys.float_info.mant_dig) - 1


def _hfloat(b: bytes, seed: bytes) -> float:
    h = hashlib.sha256()
    h.update(seed)
    h.update(b)
    return float(int(h.hexdigest()[0:16], 16)) / 2**64


def is_accepted(b: bytes, probability: float, *, seed: bytes=DEFAULT_SEED) -> bool:
    """
    Test whether b is to be accepted in an imagined set of possible values which each are accepted by the given
    probability.

    Example which retains 25% of lines read from stdin::

        for line in sys.stdin:
            if is_accepted(line.encode('utf-8'), 0.25):
                sys.stdout.write(line)

    :param b: The bytes to hash.
    :param probability: The probability of a given b being considered accepted. Must be in range [0, 1].
    :param seed: Seed to hash prior to hashing b.

    :return: Whether b is accepted.
    """
    if probability < 0.0:
        raise ValueError('probability must be >= 0.0'.format(probability))
    if probability > 1.0:
        raise ValueError('probability must be <= 1.0'.format(probability))

    return _hfloat(b, seed) < probability


def range(b: bytes, stop: int, *, start: Optional[int]=None, seed: bytes=DEFAULT_SEED) -> int:
    """
    Select an integer in a range by hashing b.

    Example partitioned filtering of a workload on stdin assuming this is partition 3 out of 10::

        for line in sys.stdin:
            if select_n(line.encode('utf-8'), 10) == 3:
                sys.stdout.write(line)

    The difference between stop and start must be sufficiently small to be exactly representable as a
    float (no larger than ``2**(sys.float_info.mant_dig) - 1``).

    :param b: The bytes to hash.
    :param stop: The *exclusive* end of the range of integers among which to select.
    :param start: The *inclusive* start of the range of integers among which to select.
    :param seed: Seed to hash prior to hashing b.

    :return: The selected integer.
    """
    if start is None:
        start = 0

    if stop <= start:
        raise ValueError('stop ({}) must be > start ({})'.format(stop, start))

    if stop - start > _MAX_FLOAT_REPRESENTABLE_INT:
        raise ValueError('stop-start must be <= {} due to limitations of floats',
                         _MAX_FLOAT_REPRESENTABLE_INT)

    return int(start + math.floor((stop - start) * _hfloat(b, seed)))


BucketType = TypeVar('BucketType')


def choice(b: bytes, seq: Sequence[BucketType], *, seed: bytes=DEFAULT_SEED) -> BucketType:
    """
    Select one of the elements in seq based on the hash of b.

    Example partitioning of input on stdin into buckets::

        bucketed_lines = {}  # type: Dict[int, str]
        for line in sys.stdin:
            buckets[select_bucket(b, [0, 1, 2, 3, 4, 5])] = line

    :param b: The bytes to hash.
    :param seq: The sequence from which to select an element. Must be non-empty, or, ValueError is raised.
    :param seed: Seed to hash prior to hashing b.

    :raise ValueError: If seq is empty.

    :return: The appropriate bucket.
    """
    if not seq:
        raise ValueError('non-empty sequence required')

    return seq[range(b, len(seq), seed=seed)]
