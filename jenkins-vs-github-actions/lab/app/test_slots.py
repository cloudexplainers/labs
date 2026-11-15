from slots import free_slots


def test_empty_day_has_eight_slots():
    assert len(free_slots([])) == 8


def test_booked_hours_are_not_free():
    assert free_slots([9, 10, 16]) == [11, 12, 13, 14, 15]
