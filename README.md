# bitbracket

A simulator for binary tree like, single elimination brackets. 

## Summary

bitbracket is a module for running tournament simulations. A _bitbracket_ is an integer that represents the outcome of each game in the tournament. This compact storage method is useful when running many simulations.

bitbracket is very easily adaptable to any project. All that is needed is team objects, and a matchup function.

## Usage

### Simulating Outcomes

A simulation is run with the simulate function.

    bitbracket.simulate(teams, matchup, n=1000)

Inputs and outputs are discussed below. 

#### Teams

The teams input is a list of team objects. A team object could be instances of a custom class, dictionaries of team stats, just team names, etc. The number of teams needs to be a power of 2, and each team object needs to be the same type.

The teams should be ordered according to their bracket position. For example, consider this ordering of teams: 
1. Team 1
2. Team 8
3. Team 4
4. Team 5
5. Team 3
6. Team 6
7. Team 2
8. Team 7

In this bracket, the first round consists of: 
1. Team 1 vs. Team 8
2. Team 4 vs. Team 5
3. Team 3 vs. Team 6
4. Team 2 vs. Team 7

The second round is played with the winners of the first round games, again taking two at a time.

#### Matchup Function

The matchup argument should be a function that takes two team objects as inputs, and returns a 0 if the first team wins, or else a 1 (second team wins). For example, supposing the team objects had a seed attribute and you wanted a chalk bracket:

    matchup = lambda x, y: int(x.seed > y.seed)

Say x was seeded 5 and y was seeded 12. x.seed > y.seed is False, and int(False) = 0 meaning the 5 seed wins. If the teams were input in the reverse order, int(12 > 5) = 1, meaning the 5 seed wins again.

Right now, the output is always checked to ensure a result equal to 0 or 1, but this may be removed in the future to improve performance. So, be sure this is all your function can return.

Normally this function would calculate the odds of victory based on team stats, then add some element of randomness before retuning a winner. If the outcome of the matchup function is _always_ the same, then the resulting bracket will always be the same.

#### Number of Iterations

The last argument is the number of times to simulate the tournament. By default, it's only 1000. 

#### Output 

After the simulations are complete, the simulate function returns a Counter object. The Counter class is defined in python's standard collections module. Basically, it's a dictionary where the keys are things that were counted, and the values are the count. In this case, the keys are bitbrackets.

Counter comes with a most_common() method that will likely come in handy after running the simulation. No need to reinvent the wheel!

### Interpreting Results

The integer bitbrackets are not very legible, but they can be translated easily.

    bitbracket.translate(bb, teams)

This function takes a bitbracket and the list of team objects provided to the simulator and returns nested lists of team objects corresponding to the teams that made it to each round. The first nested list is all teams, and the last nested list is the champion.

## Parallel Simulations

There is no built-in function to run simulations in parallel, but this can be done very easily using the multiprocessing module. The returned Counters can be added together. 
