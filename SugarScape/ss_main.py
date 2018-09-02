"""
Main module of the sugarscape simulation
Updates:
    07-06-2016: First Draft
    07-07-2017: Compatible with unified gui
"""

import cab.complex_automaton as cab_sys
import cab.util.logging as cab_log

from abm.ss_agent_manager import SSAgentManager
from ca.ss_cell import WorldCell
from ss_global_constants import GC
from util.ss_hex_terrain_gen import TerrainGenerator

__author__ = 'Michael Wagner'

if __name__ == '__main__':
    cab_log.set_log_debug()
    gc = GC()
    pc = WorldCell(0, 0, gc)
    pa = SSAgentManager(None, None, gc)

    tg = TerrainGenerator(gc)
    pc.set_terrain_gen(tg)

    # Use assets to initialize simulation system.

    simulation = cab_sys.ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa)


    # Run the simulation
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
