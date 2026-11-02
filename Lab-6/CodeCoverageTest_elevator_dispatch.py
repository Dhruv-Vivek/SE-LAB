import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---- starter tests ----
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ---- next_direction: executes every line ----
def test_up_with_requests_above_keeps_going_up():
    assert next_direction(3, "up", [5, 7]) == "up"


def test_up_with_only_requests_below_reverses():
    assert next_direction(5, "up", [2]) == "down"


def test_up_with_no_requests_goes_idle():
    assert next_direction(5, "up", []) == "idle"


def test_down_with_requests_below_keeps_going_down():
    assert next_direction(5, "down", [2]) == "down"


def test_down_with_only_requests_above_reverses():
    assert next_direction(2, "down", [6]) == "up"


def test_down_with_no_requests_goes_idle():
    assert next_direction(5, "down", []) == "idle"


def test_idle_with_request_above_goes_up():
    assert next_direction(3, "idle", [8]) == "up"


def test_idle_with_request_below_goes_down():
    assert next_direction(8, "idle", [3]) == "down"


# ---- door_action ----
def test_overload_when_load_exceeds_limit():
    assert door_action(700, False, False) == "overload"


def test_blocked_door_reopens():
    assert door_action(400, True, False) == "reopen"


def test_normal_close():
    assert door_action(400, False, False) == "close"


# ---- pick_elevator ----
def test_pick_nearest_idle_car():
    cars = [("A", 1, True), ("B", 9, True)]
    assert pick_elevator(cars, 8) == "B"
