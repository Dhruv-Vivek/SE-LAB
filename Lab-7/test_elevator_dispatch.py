from hypothesis import given, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent

# Anything a caller (or attacker) might pass in: text, None, numbers, bytes, containers
ANYTHING = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.integers()),
)

# Text shaped like the real formats, so Hypothesis gets past the first split
FLOORISH = st.text(alphabet="0123456789-+,>_ ofx\t\n٣", max_size=30)


@given(ANYTHING | FLOORISH)
def test_parse_request_no_crash(s):
    try:
        parse_request(s)
    except Exception as e:
        assert False, f"parse_request crashed with: {e!r}"


@given(ANYTHING | FLOORISH)
def test_total_travel_no_crash(s):
    try:
        total_travel(s)
    except Exception as e:
        assert False, f"total_travel crashed with: {e!r}"


@given(ANYTHING | FLOORISH)
def test_load_percent_no_crash(s):
    try:
        load_percent(s)
    except Exception as e:
        assert False, f"load_percent crashed with: {e!r}"


# ---- Property checks: valid input must give correct output ----

@given(st.integers(-1000, 1000), st.integers(-1000, 1000))
def test_parse_request_roundtrip(a, b):
    assert parse_request(f"{a}->{b}") == (a, b)


@given(st.lists(st.integers(-1000, 1000), min_size=1, max_size=30))
def test_total_travel_valid(floors):
    result = total_travel(",".join(map(str, floors)))
    expected = sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))
    assert result == expected and result >= 0


@given(st.integers(0, 10**6), st.integers(1, 10**6))
def test_load_percent_valid(load, cap):
    assert load_percent(f"{load} of {cap}") == load * 100 // cap


@given(st.integers(0, 10**6))
def test_load_percent_zero_capacity_rejected(load):
    assert load_percent(f"{load} of 0") is None
