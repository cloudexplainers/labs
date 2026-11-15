"""Free grooming slots for one day at Ana's dog grooming salon."""

OPEN, CLOSE = 9, 17          # the salon opens 9:00, last slot starts 16:00


def free_slots(booked):
    """Hours still free today, given the hours already booked."""
    return [h for h in range(OPEN, CLOSE - 1) if h not in booked]
