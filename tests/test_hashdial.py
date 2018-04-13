import hashdial
import time

from typing import Dict


def test_hfloat_distribution() -> None:
    NUM_SAMPLES = 10000
    NUM_BUCKETS = 10

    buckets = {}  # type: Dict[int, int]
    for n in range(NUM_SAMPLES):
        f = hashdial._hfloat('{}'.format(n).encode('utf-8'))
        bucket = int(f * NUM_BUCKETS)
        buckets[bucket] = buckets.get(bucket, 0) + 1

    # Assert that all buckets are within 10% of target ratio.
    for _, count in buckets.items():
        assert count > float(1) / NUM_BUCKETS * NUM_SAMPLES * 0.9
        assert count < float(1) / NUM_BUCKETS * NUM_SAMPLES * 1.1
