import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---- starter tests ----
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ---- next_direction: both outcomes of every decision ----
@pytest.mark.parametrize("current, direction, requests, expected", [
    # direction == "up": above True / below True / neither
    (3, "up", [5, 7], "up"),
    (5, "up", [2], "down"),
    (5, "up", [], "idle"),
    # direction == "down": below True / above True / neither
    (5, "down", [2], "down"),
    (2, "down", [6], "up"),
    (5, "down", [], "idle"),
    # direction == "idle" (fall-through): above / below / neither
    (3, "idle", [8], "up"),
    (8, "idle", [3], "down"),
    (3, "idle", [], "idle"),
])
def test_next_direction_all_branches(current, direction, requests, expected):
    assert next_direction(current, direction, requests) == expected


def test_up_prefers_up_even_when_requests_on_both_sides():
    assert next_direction(5, "up", [2, 9]) == "up"


def test_down_prefers_down_even_when_requests_on_both_sides():
    assert next_direction(5, "down", [2, 9]) == "down"


def test_request_on_current_floor_is_ignored():
    # f == current is neither above nor below
    assert next_direction(4, "up", [4]) == "idle"
    assert next_direction(4, "down", [4]) == "idle"
    assert next_direction(4, "idle", [4]) == "idle"


def test_unknown_direction_behaves_like_idle():
    assert next_direction(3, "sideways", [8]) == "up"


# ---- door_action: each condition True and False, plus priority ----
def test_overload_when_load_exceeds_limit():
    assert door_action(700, False, False) == "overload"


def test_load_at_limit_is_not_overload():
    assert door_action(630, False, False) == "close"


def test_load_just_over_limit_is_overload():
    assert door_action(631, False, False) == "overload"


def test_blocked_door_reopens():
    assert door_action(400, True, False) == "reopen"


def test_normal_close():
    assert door_action(400, False, False) == "close"


def test_emergency_beats_overload_and_blocked():
    assert door_action(900, True, True) == "hold_open"


def test_overload_beats_blocked():
    assert door_action(900, True, False) == "overload"


# ---- pick_elevator: loop never runs / runs, is_idle both ways, gap< best both ways ----
def test_no_cars_returns_none():
    assert pick_elevator([], 5) is None


def test_single_car_is_chosen():
    assert pick_elevator([("A", 1, True)], 5) == "A"


def test_pick_nearest_idle_car_when_later_car_is_closer():
    assert pick_elevator([("A", 1, True), ("B", 9, True)], 8) == "B"


def test_keeps_first_car_when_later_car_is_farther():
    assert pick_elevator([("A", 7, True), ("B", 1, True)], 8) == "A"


def test_tie_keeps_first_car():
    assert pick_elevator([("A", 2, True), ("B", 6, True)], 4) == "A"


def test_busy_car_penalised_so_farther_idle_car_wins():
    # A: |3-4| + 5 = 6 ; B: |9-4| = 5
    assert pick_elevator([("A", 3, False), ("B", 9, True)], 4) == "B"


def test_busy_car_still_wins_when_much_closer():
    # A: |4-4| + 5 = 5 ; B: |15-4| = 11
    assert pick_elevator([("A", 4, False), ("B", 15, True)], 4) == "A"
