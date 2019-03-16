"""
A simulator for binary tree like, single elimination brackets.

Functions:
    champion: Return the champion of a bitbracket
    simulate: Run n simulations of a tournament, return a Counter.
    translate: Decode a bitbracket into tournament rounds.
"""
import collections


def champion(bitbracket, teams):
    """Return the winning team of the bitbracket."""
    bracket = translate(bitbracket, teams)
    return bracket[-1][0]


def simulate(teams, matchup, n=1000):
    """Simulate the tournament n times, record bitbracket outcomes.

    Note that the returned Counter object has a most_common() method
    to sort all by frequency. See python collections docs for more info.

    Args:
        teams: A list/tuple of team objects.
        matchup: A function that takes two team objects and returns a 0
                 if the first team wins, else a 1 (second team wins).
        n: The number of simulations to run; default is 1000.

    Returns:
        A collections.Counter object with bitbracket keys.
    """
    _validate_teams(teams)
    _validate_matchup(matchup, teams)
    _validate_n(n)
    
    counter = collections.Counter()

    for _ in range(n):
        bitbracket = _simulation_iteration(teams, matchup)
        counter[bitbracket] += 1

    return counter


def translate(bitbracket, teams):
    """Convert a bitbracket into nested lists of teams."""
    _validate_bitbracket(bitbracket)
    _validate_teams(teams)
    
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


def _simulation_iteration(teams, matchup):
    """Run a single simulation and return a bitbracket."""
    teams = list(teams)

    bitbracket = 0
    while len(teams) > 1:
        for i in range(len(teams)//2):
            winner = matchup(teams[i], teams[i+1])
            assert winner == 0 or winner == 1
            teams.pop(i + (1 - winner))
            bitbracket <<= 1
            bitbracket += winner

    return bitbracket


def _validate_bitbracket(bitbracket):
    """Ensure the bitbracket is an integer."""
    if type(bitbracket) is not int:
        raise TypeError('bitbracket should be an integer.')


def _validate_n(n):
    """Ensure the number of iterations is valid."""
    try:
        assert type(n) is int
        assert n > 0
    except AssertionError:
        raise ValueError('n must be an integer >= 1!')


def _validate_matchup(matchup, teams):
    """Ensure the matchup function works with team objects."""
    if not callable(matchup):
        raise TypeError('matchup must be a function!')
    
    try:
        winner = matchup(*teams[:2])
    except BaseException:
        raise ValueError('p must take two team object inputs!')

    if winner not in (0, 1):
        raise ValueError('matchup should return 0 or 1!')


def _validate_teams(teams):
    """Ensure the teams input is valid."""
    if type(teams) not in (list, tuple):
        raise TypeError('teams must be a list or tuple of team objects!')

    num_teams = len(teams)
    if num_teams < 2 or num_teams & (num_teams - 1):
        raise ValueError('Invalid number of teams!')

    if len(set(map(type, teams))) > 1:
        raise TypeError('Team objects must all be the same type!')


if __name__ == '__main__':
    pass
