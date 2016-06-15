"""
Main module of the sugarscape simulation
Updates:
    07-06-2016: First Draft
"""

__author__ = 'Michael Wagner'


from cab.cab_system import ComplexAutomaton

# from abm.ss_agent import HiveAgent
from abm.ss_agent import SSAgentManager
from ca.ss_cell import WorldCell
from ss_global_constants import GC
from util.ss_io_handling import EventHandler
from util.ss_visualization import Visualizer
from util.ss_terrain_gen import TerrainGenerator


if __name__ == '__main__':

    gc = GC()
    pc = WorldCell(0, 0, gc)
    pa = SSAgentManager(None, None, gc)
    ph = EventHandler(None)
    pv = Visualizer(gc, None, None)

    tg = TerrainGenerator(gc.DIM_X, gc.DIM_Y)
    pc.set_terrain_gen(tg)

    # Use assets to initialize simulation system.

    # simulation = ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa, proto_handler=ph, proto_visualizer=pv)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa, proto_handler=ph, proto_visualizer=pv)

    # Run the simulation
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
