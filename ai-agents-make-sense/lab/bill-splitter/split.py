"""Split a restaurant bill between friends."""


def split_bill(total, people, tip_percent):
    """Return what each person pays, tip included, rounded to cents."""
    with_tip = total + total * tip_percent
    return round(with_tip / people, 2)
