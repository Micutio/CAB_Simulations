# CAB_Simulations
This repository contains a collection of cellular automata / agent-based simulations using the
ComplexAutomataBase (CAB) framework.


## Foraging Ant

### Description

Foraging Ant describes the teamwork of ants on their mission to find food and deliver it back to
their anthill. By using two sorts of pheromones to mark their trails back and forth, these tiny
soldiers manage to implicitly communicate with one another and eventually create a nearly optimized
trail.

Simple features as

* individually simulated ants, acting according to only two primitive rules
* individually simulated world cells
* pheromone trails evaporating over time

lead to an organic seeming behavior and lively little anthills.

### Screenshots
![alt text](https://github.com/Micutio/CAB_Simulations/blob/master/media/ant_screenshot1.png "Foraging Ant Screenshot")



## Sugarscape [Alpha Version, Under Construction]

The Sugarscape is a world of sugar and spice. Agents will roam the land and harvest the resources
to stay alive. Agents can mate and create offspring that will carry on their genes. Simple rules
allow for complex behavior, leading to migrations, diseases, population fluctuations, trading and
more.

## Urban Development [Under Construction]

Urban Development will explore organic growth of cities or other urban ecologies by using the RICO
model, whereby urban land use is divided into three principal designations: residential, industrial
and commercial. The ultimate goal will be to find non-complex rules that lead an initial seed, of
one or more of these land uses, to grow into a plausible city shape over time.

### Version 1 - Primitive Growth

With the first version we will try to get a feeling for underlying rules of urban development.
These could be the following:

* residential zones want commerce to acquire goods and services to live
* commercial zones want industry to acquire goods to sell
* industrial zones want residents to populate their factories

It is apparent that the relationships between all three zones form a cycle. How can we derive rules
for zone growth from these observations? If we look at [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life),
it divides growth into three categories. A cell can come to life, stay alive or die, depending on
the number of living and dead neighbors. If we transfer this approach to our zones, it might look
like this:

* if an empty zone has a neighbor with a commercial zone, then it can become a residential zone
* if an empty zone has a neighbor with an industrial zone, then it can become a commercial zone
* if an empty zone has a neighbor with a residential zone, then it can become an industrial zone
* if two or more criteria are met, the empty zone chooses its new designation at random 
