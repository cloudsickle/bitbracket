"""
Tests for bitbracket.py.
"""
import os
import unittest
import sys

# Add module directory to the system path for bitbracket import.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import bitbracket


class TestChampion(unittest.TestCase):

    def test_champion(self):
        champion = bitbracket.champion(0, [1, 2, 3, 4])
        self.assertEqual(champion, 1)


class TestSimulate(unittest.TestCase):

    def test_result(self):
        teams = [1, 2, 3, 4]
        matchup = lambda x, y: 1

        c = bitbracket.simulate(teams, matchup, n=1)

        bb = list(c.keys())[0]

        self.assertEqual(bb, 0b111)

    def test_num_teams(self):
        matchup = lambda x, y: int(x > y)

        teams = list(range(5))
        with self.assertRaises(ValueError):
            bitbracket.simulate(teams, matchup)

        teams = [1]
        with self.assertRaises(ValueError):
            bitbracket.simulate(teams, matchup)

    def test_different_team_object_types(self):
        teams = [1, '2', 3.0, 4]
        matchup = lambda x, y: int(x > y)

        with self.assertRaises(TypeError):
            bitbracket.simulate(teams, matchup)

    def test_wrong_teams_type(self):
        teams = list(range(4))
        matchup = lambda x, y: int(x > y)

        bitbracket.simulate(teams, matchup, n=1)
        bitbracket.simulate(tuple(teams), matchup, n=1)

    def test_negative_n(self):
        teams = [1, 2]
        matchup = lambda x, y: int(x > y)

        with self.assertRaises(ValueError):
            bitbracket.simulate(teams, matchup, -1)

    def test_wrong_matchup_type(self):
        teams = [1, 2]
        matchup = None

        with self.assertRaises(TypeError):
            bitbracket.simulate(teams, matchup)

    def test_wrong_matchup_inputs(self):
        teams = [1, 2]
        matchup = lambda x: 0

        with self.assertRaises(ValueError):
            bitbracket.simulate(teams, matchup)

    def test_wrong_matchup_return_type(self):
        teams = [1, 2]
        matchup = lambda x: 'a'

        with self.assertRaises(ValueError):
            bitbracket.simulate(teams, matchup)


class TestTranslate(unittest.TestCase):

    def test_invalid_bitbracket(self):
        with self.assertRaises(TypeError):
            bitbracket.translate(8.0, [1, 2])

    def test_rounds(self):
        bracket = bitbracket.translate(0, [1, 2, 3, 4])

        self.assertEqual(bracket[0], [1, 2, 3, 4])
        self.assertEqual(bracket[1], [1, 3])
        self.assertEqual(bracket[2], [1])


if __name__ == '__main__':
    unittest.main()
