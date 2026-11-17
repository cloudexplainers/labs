import unittest

from bookings import price


class PriceTest(unittest.TestCase):
    def test_full_price(self):
        self.assertEqual(price("wheel"), 45)

    def test_student_price(self):
        self.assertEqual(price("wheel", student=True), 40.5)


if __name__ == "__main__":
    unittest.main()
