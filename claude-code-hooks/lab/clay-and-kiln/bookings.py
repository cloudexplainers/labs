"""Class bookings for the Clay & Kiln pottery studio."""

PRICES = {"wheel": 45, "handbuilding": 35, "glazing": 25}
STUDENT_DISCOUNT = 0.10


def price(class_name, student=False):
    """Price of one class, in dollars."""
    cost = PRICES[class_name]
    if student:
        cost = cost * (1 - STUDENT_DISCOUNT)
    return round(cost, 2)
