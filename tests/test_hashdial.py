import pytest

from typing import Dict  # noqa (mypy/lint fight)

import hashdial


def test_hfloat_distribution() -> None:
    NUM_SAMPLES = 10000
    NUM_BUCKETS = 10

    buckets = {}  # type: Dict[int, int]
    for n in range(NUM_SAMPLES):
        f = hashdial._hfloat('{}'.format(n).encode('utf-8'), seed=b'')
        assert f >= 0.0
        assert f <= 1.0
        bucket = int(f * NUM_BUCKETS)
        buckets[bucket] = buckets.get(bucket, 0) + 1

    # Assert that all buckets are within 10% of target ratio.
    for _, count in buckets.items():
        assert count > float(1) / NUM_BUCKETS * NUM_SAMPLES * 0.9
        assert count < float(1) / NUM_BUCKETS * NUM_SAMPLES * 1.1


def test_hfloat_uses_seed() -> None:
    assert hashdial._hfloat(b't', seed=b'') != hashdial._hfloat(b't', seed=b'something')


def test_is_accepted_distribution() -> None:
    PROBABILITY = 0.25
    NUM_SAMPLES = 1000

    value_count = {}  # type: Dict[bool,int]
    for n in range(NUM_SAMPLES):
        b = hashdial.is_accepted(PROBABILITY, '{}'.format(n).encode('utf-8'))
        value_count[b] = value_count.get(b, 0) + 1

    assert value_count[True] > PROBABILITY * NUM_SAMPLES * 0.9
    assert value_count[True] < PROBABILITY * NUM_SAMPLES * 1.1


def test_is_accepted_seed() -> None:
    assert hashdial.is_accepted(0.5, b't') != hashdial.is_accepted(0.5, b't', seed=b'test2')


def test_select_n_distribution() -> None:
    NUM_SAMPLES = 10000

    values = {}  # type: Dict[int, int]

    for n in range(NUM_SAMPLES):
        selected = hashdial.select_n(2, '{}'.format(n).encode('utf-8'), start=-1)
        values[selected] = values.get(selected, 0) + 1

    assert set(values.keys()) == {-1, 0, 1}

    for val in [-1, 0, 1]:
        assert values[val] > NUM_SAMPLES * 0.33 * 0.9
        assert values[val] < NUM_SAMPLES * 0.33 * 1.1


def test_select_n_seed() -> None:
    assert hashdial.select_n(2, b't') != hashdial.select_n(2, b't', seed=b'test2')


def test_select_n_large_diff() -> None:
    with pytest.raises(ValueError):
        hashdial.select_n(2**63, b'')
    with pytest.raises(ValueError):
        hashdial.select_n(start=-(2**63), stop=0, b=b'')


def test_select_bucket() -> None:
    NUM_SAMPLES = 10000

    values = {}  # type: Dict[int, int]

    for n in range(NUM_SAMPLES):
        selected = hashdial.select_bucket([-1, 0, 1], '{}'.format(n).encode('utf-8'))
        values[selected] = values.get(selected, 0) + 1

    assert set(values.keys()) == {-1, 0, 1}

    for val in [-1, 0, 1]:
        assert values[val] > NUM_SAMPLES * 0.33 * 0.9
        assert values[val] < NUM_SAMPLES * 0.33 * 1.1


def test_select_bucket_seed() -> None:
    assert hashdial.select_bucket([0, 1], b't') != hashdial.select_bucket([0, 1], b't', seed=b'test2')
