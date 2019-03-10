# bitbracket

A simulator for binary tree like, single elimination brackets. 

## Summary

bitbracket is a module for running tournament simulations. A _bitbracket_ is an integer that represents the outcome of each game in the tournament. This compact storage method is useful when running many simulations.

bitbracket is very easily adaptable to any project. All that is needed is team objects, and a probability function.

## Usage

### Simulating Outcomes

A simulation is run with the simulate function.

    bitbracket.simulate(teams, p, n=1000)

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

#### Probability Function

The p argument should be a function that takes two team objects as inputs, and returns the probability that the first team wins. For example, supposing the team objects had a seed attribute and you wanted a chalk bracket:

    p = lambda x, y: int(x.seed <= y.seed)

There is no check to ensure that the output of p is always in [0, 1], so don't mess up!

Note that this function is supposed to return an _expectation_. Bitbracket calculates a random probability and compares that to the expectation to determine the winner. You can override this by calculating your own winner in p(), then returning 0 or 1 to force the outcome.

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
