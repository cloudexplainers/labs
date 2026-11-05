import unittest
from split import split_bill


class TestSplitBill(unittest.TestCase):
    def test_no_tip(self):
        self.assertEqual(split_bill(100, 4, 0), 25.0)

    def test_ten_percent_tip(self):
        self.assertEqual(split_bill(100, 4, 10), 27.5)


if __name__ == "__main__":
    unittest.main()
