import unittest
from numpy import inf
import Interval

class Test(unittest.TestCase):
    def setUp(self):
        self.a = Interval(1,5)
        self.b = Interval(3,7)
        self.c = Interval(0, 4)
        self.d = Interval(-3, 0)
        self.e = Interval(-4, 3)
        self.f = Interval(-8, -4)
        self.g = Interval(-inf, 5)
        self.h = Interval(-inf, -3)
        self.i = Interval(-4, inf)
        self.j = Interval(6, inf)
        self.k = Interval(-inf, inf)
        self.l = Interval(0,0)

    def test_ctor(self):
        # Check lower / upper bounds of the intervals.. tedious..
        self.assertEqual(0,0)

