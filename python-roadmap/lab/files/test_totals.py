from totals import revenue, totals

ORDERS = [{"item": "cinnamon bun", "qty": "3", "price": "1.10"}]


def test_totals():
    assert totals(ORDERS) == {"cinnamon bun": 3}


def test_revenue():
    assert revenue(ORDERS) == {"cinnamon bun": 3.30}
