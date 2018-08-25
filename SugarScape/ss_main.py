"""
Main module of the sugarscape simulation
Updates:
    07-06-2016: First Draft
    07-07-2017: Compatible with unified gui
"""

from cab.cab_system import ComplexAutomaton
from cab.util.cab_logging import set_log_trace

from abm.ss_agent_manager import SSAgentManager
from ca.ss_cell import WorldCell
from ss_global_constants import GC
from util.ss_hex_terrain_gen import TerrainGenerator

__author__ = 'Michael Wagner'

if __name__ == '__main__':
    set_log_trace()
    gc = GC()
    pc = WorldCell(0, 0, gc)
    pa = SSAgentManager(None, None, gc)

    tg = TerrainGenerator(gc)
    pc.set_terrain_gen(tg)

    # Use assets to initialize simulation system.

    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa)


    # Run the simulation
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
