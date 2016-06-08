"""
Main module of the sugarscape simulation
Updates:
    07-06-2016: First Draft
"""

__author__ = 'Michael Wagner'


from cab.cab_system import ComplexAutomaton

from abm.fa_agent import HiveAgent
from ca.fa_cell import WorldCell
from fa_global_constants import GC
from util.fa_io_handling import EventHandler
from util.fa_visualization import Visualizer


if __name__ == '__main__':

    gc = GC()
    pc = WorldCell(0, 0, gc)
    #pa = HiveAgent(0, 0, gc)
    ph = EventHandler(None)
    pv = Visualizer(gc, None, None)


    # Use assets to initialize simulation system.

    # simulation = ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa, proto_handler=ph, proto_visualizer=pv)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)

    # Run the simulation
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
