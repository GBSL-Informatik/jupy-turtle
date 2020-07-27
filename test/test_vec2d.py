import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import unittest
# from unittest.mock import patch
from math import pi
from gturtle import Vec2D
# import sys
# import contextlib
# from io import StringIO

class TestVec2D(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    def test_norm(self):
        self.assertEqual(1, Vec2D(1, 0).norm())
        self.assertEqual(3, Vec2D(3, 0).norm())
        self.assertEqual(5, Vec2D(4, 3).norm())

    def test_normalized(self):
        self.assertEqual(Vec2D(1, 0), Vec2D(1, 0).normalized())
        self.assertEqual(Vec2D(1, 0), Vec2D(3, 0).normalized())
        self.assertEqual(Vec2D(4, 3).normalized(), Vec2D(1, 3/4).normalized())

    def test_rotate(self):
        self.assertAlmostEqual(Vec2D(0, 1).x, Vec2D(1, 0).rotate(90).x)
        self.assertAlmostEqual(Vec2D(0, 1).y, Vec2D(1, 0).rotate(90).y)

        self.assertAlmostEqual(Vec2D(0, 10).x, Vec2D(10, 0).rotate(90).x)
        self.assertAlmostEqual(Vec2D(0, 10).y, Vec2D(10, 0).rotate(90).y)

        self.assertAlmostEqual(Vec2D(0, -1).x, Vec2D(1, 0).rotate(270).x)
        self.assertAlmostEqual(Vec2D(0, -1).y, Vec2D(1, 0).rotate(270).y)

        # clockwise
        self.assertAlmostEqual(Vec2D(0, -1).x, Vec2D(1, 0).rotate(90, False).x)
        self.assertAlmostEqual(Vec2D(0, -1).y, Vec2D(1, 0).rotate(90, False).y)

        self.assertAlmostEqual(Vec2D(0, -10).x, Vec2D(10, 0).rotate(90, False).x)
        self.assertAlmostEqual(Vec2D(0, -10).y, Vec2D(10, 0).rotate(90, False).y)

        self.assertAlmostEqual(Vec2D(0, 1).x, Vec2D(1, 0).rotate(270, False).x)
        self.assertAlmostEqual(Vec2D(0, 1).y, Vec2D(1, 0).rotate(270, False).y)

if __name__ == '__main__':
    unittest.main()
