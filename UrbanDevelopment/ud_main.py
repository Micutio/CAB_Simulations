
from cab.complex_automaton import ComplexAutomaton
import cab.util.rng as cab_rng

from ud_global_constants import GC
from abm.ud_agent import UrbanAgent
from ca.ud_cell import WorldCell
from util.ud_terrain_gen import TerrainGenerator

"""
Main module of the urban development simulation.
This shall be used to experiment with growth models of cities or urban areas in
general.

[Under construction]

Idea for v1.0:
    Three different types of land use (residential, commercial, industrial).
    Residental cells grow/are created when there is a lot of commerce.
    Commercial cells grow/are created when there is a lot of industry.
    Industrial cells grow/are created when there is a lot of residents.
    Residental cells are negatively impacted by nearby industrial cells.

    Look into the following entities and how they can be incorporated:
    - roads
    |--> making distant cells available
    - natural resources
    |--> create incentives for settlements
    |--> create boost for industry
    - terrain
    |--> promote/inhibit spreading rate of cells
    - agents
    |--> flow of goods and people

"""

__author__ = 'Michael Wagner'
__version__ = '1.0'


if __name__ == '__main__':

    cab_rng.seed_RNG(1234)

    gc = GC()
    pc = WorldCell(0, 0, gc)
    pa = UrbanAgent(0, 0, gc)

    tg = TerrainGenerator(gc)
    pc.set_terrain_gen(tg)

    # Use assets to initialize simulation system.
    simulation = ComplexAutomaton(gc, proto_cell=pc)

    # Run the simulation
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
