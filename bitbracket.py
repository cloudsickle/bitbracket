"""
bitbracket - A simulator for symmetric, single elimination brackets.

bitbracket works independently from team data and winning probability
functions. This means that you can adapt it easily to your own project.

To use bitbracket, you need a list/tuple of team data, and a probability
function to determine the likelihood of one team beating another.

There are only three functions to be aware of in bitbracket:

    champion(bitbracket, teams)
        Take a bitbracket and list of team data and return the team data
        of the champion.

    simulate(teams, p, n=1000)
        Take a list of team data, a probability function, and a number
        of iterations and return a collections.Counter with bitbracket
        keys. Use the most_common() function on the Counter to sort the
        results or pull the N most common results.

    translate(bitbracket, teams)
        Take a bitbracket and list of team data and return nested lists
        of teams representing the rounds of the tournament. The first
        entry contains all teams, the last entry is a list containing
        only the champion.

Example usage:

    >>> import bitbracket
    >>> teams = list(range(64))
    >>> def p(team_1, team_2):
            return 0.5
    >>> bbs = bitbracket.simulate(teams, p, n=1000)
    >>> bb, occur = bbs.most_common(1)[0]
    >>> champ = bitbracket.champion(bb, teams)
    >>> pct = occur/1000
    >>> print('{} wins it all {:.1%} of the time.'.format(champ, pct))
    >>> bracket = bitbracket.translate(bb, teams)
    >>> for rnd in bracket:
            print(rnd)
"""
import collections
import random


def champion(bitbracket, teams):
    """Return the winning team of the bitbracket."""
    bracket = translate(bitbracket, teams)
    return bracket[-1][0]


def simulate(teams, p, n=1000):
    """Create bitbrackets for the provided teams.

    teams is a list/tuple of team data. This can be whatever team data
    you have for your application; that may just be a string team name,
    or it could be an instance of a Team class, etc.

    p is a function input that takes two entries from teams and returns
    the probability that the first team wins. For example:

        def p(team_1, team_2):
            return team_2.rank/(team_1.rank + team_2.rank)

    n is the number of simulations to perform.

    Returns a collections.Counter where keys are bitbrackets, and
    values are the number of times the bitbracket appeared.

    One of the most common post-simulation operations is to sort the
    brackets by likelihood. This can be done using the .most_common()
    method on the return Counter object. No need to reinvent the wheel!
    """
    counter = collections.Counter()

    for _ in range(n):
        bitbracket = _simulation_iteration(teams, p)
        counter[bitbracket] += 1

    return counter


def translate(bitbracket, teams):
    """Convert a bitbracket into a nested lists of teams."""
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
    """Run a single simulation, return a bitbracket."""
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
