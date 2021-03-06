from typing import Dict  # noqa (mypy/lint fight)

import pytest

import hashdial


def test_hfloat_distribution() -> None:
    NUM_SAMPLES = 10000
    NUM_BUCKETS = 10

    buckets = {}  # type: Dict[int, int]
    for n in range(NUM_SAMPLES):
        f = hashdial._hfloat("{}".format(n).encode("utf-8"), seed=b"")
        assert f >= 0.0
        assert f <= 1.0
        bucket = int(f * NUM_BUCKETS)
        buckets[bucket] = buckets.get(bucket, 0) + 1

    # Assert that all buckets are within 10% of target ratio.
    for _, count in buckets.items():
        assert count > float(1) / NUM_BUCKETS * NUM_SAMPLES * 0.9
        assert count < float(1) / NUM_BUCKETS * NUM_SAMPLES * 1.1


def test_hfloat_uses_seed() -> None:
    assert hashdial._hfloat(b"t", seed=b"") != hashdial._hfloat(b"t", seed=b"something")


def test_decide() -> None:
    PROBABILITY = 0.25
    NUM_SAMPLES = 1000

    value_count = {}  # type: Dict[bool,int]
    for n in range(NUM_SAMPLES):
        b = hashdial.decide("{}".format(n).encode("utf-8"), PROBABILITY)
        value_count[b] = value_count.get(b, 0) + 1

    assert value_count[True] > PROBABILITY * NUM_SAMPLES * 0.9
    assert value_count[True] < PROBABILITY * NUM_SAMPLES * 1.1


def test_decide_bad_probability() -> None:
    hashdial.decide("".encode(), 0.5)

    with pytest.raises(ValueError) as exc_info:
        hashdial.decide("".encode(), -0.5)
    assert str(exc_info.value) == "probability (-0.5) must be >= 0.0"

    with pytest.raises(ValueError) as exc_info:
        hashdial.decide("".encode(), 1.5)
    assert str(exc_info.value) == "probability (1.5) must be <= 1.0"


def test_decide_seed() -> None:
    assert hashdial.decide(b"t", 0.5) != hashdial.decide(b"t", 0.5, seed=b"test2")


def test_range_distribution() -> None:
    NUM_SAMPLES = 10000

    values = {}  # type: Dict[int, int]

    for n in range(NUM_SAMPLES):
        selected = hashdial.range("{}".format(n).encode("utf-8"), 2, start=-1)
        values[selected] = values.get(selected, 0) + 1

    assert set(values.keys()) == {-1, 0, 1}

    for val in [-1, 0, 1]:
        assert values[val] > NUM_SAMPLES * 0.33 * 0.9
        assert values[val] < NUM_SAMPLES * 0.33 * 1.1


def test_range_seed() -> None:
    assert hashdial.range(b"t", 2) != hashdial.range(b"t", 2, seed=b"test2")


def test_range_large_diff() -> None:
    with pytest.raises(ValueError):
        hashdial.range(b"", 2 ** 63)
    with pytest.raises(ValueError):
        hashdial.range(start=-(2 ** 63), stop=0, key=b"")


def test_select() -> None:
    NUM_SAMPLES = 10000

    values = {}  # type: Dict[int, int]

    for n in range(NUM_SAMPLES):
        selected = hashdial.select("{}".format(n).encode("utf-8"), [-1, 0, 1])
        values[selected] = values.get(selected, 0) + 1

    assert set(values.keys()) == {-1, 0, 1}

    for val in [-1, 0, 1]:
        assert values[val] > NUM_SAMPLES * 0.33 * 0.9
        assert values[val] < NUM_SAMPLES * 0.33 * 1.1


def test_select_seed() -> None:
    assert hashdial.select(b"t", [0, 1]) != hashdial.select(b"t", [0, 1], seed=b"test2")


def test_select_empty_seq() -> None:
    with pytest.raises(ValueError):
        hashdial.select(b"", [])
