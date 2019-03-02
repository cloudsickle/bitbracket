"""
bitbracket - A simulator for symmetric, single elimination brackets.

There are only three functions to be aware of in bitbracket:

    champion(bitbracket, teams)
        Take a bitbracket and list of team objects and return the team
        object corresponding to the champion.

    simulate(teams, p, n=1000)
        Take a list of team objects, a probability function, and a
        number of iterations and return a collections.Counter with
        bitbracket keys.

    translate(bitbracket, teams)
        Take a bitbracket and list of team objects and return nested
        lists of teams representing the rounds of the tournament. The
        first entry contains all teams, the last entry is a list
        containing only the champion.
"""
import collections
import random


def champion(bitbracket, teams):
    """Return the winning team of the bitbracket."""
    bracket = translate(bitbracket, teams)
    return bracket[-1][0]


def simulate(teams, p, n=1000):
    """Simulate the tournament n times, record bitbracket outcomes.

    Note that the returned Counter object has a most_common() method
    to sort all by frequency. See python collections docs for more info.

    Args:
        teams: A list/tuple of team objects.
        p: A function that takes two team objects and returns the
            probability that the first team beats the second.
        n: The number of simulations to run; default is 1000.

    Returns:
        A collections.Counter object with bitbracket keys.
    """
    counter = collections.Counter()

    for _ in range(n):
        bitbracket = _simulation_iteration(teams, p)
        counter[bitbracket] += 1

    return counter


def translate(bitbracket, teams):
    """Convert a bitbracket into nested lists of teams."""
    teams = list(teams)

    bracket = [teams.copy()]
    while len(teams) > 1:
        winning_teams = []
        for i in range(len(teams)//2):
            winner = bitbracket & 1
            winning_teams.append(teams[i + winner])
            teams.pop(i + (1 - winner))
            bitbracket >>= 1
        bracket.append(winning_teams)

    return bracket


def _simulation_iteration(teams, p):
    """Run a single simulation and return a bitbracket."""
    teams = list(teams)

    bitbracket = 0
    while len(teams) > 1:
        for i in range(len(teams)//2):
            winner = int(random.random() < p(teams[i], teams[i+1]))
            teams.pop(i + (1 - winner))
            bitbracket <<= 1
            bitbracket += winner

    return bitbracket


if __name__ == '__main__':
    pass
