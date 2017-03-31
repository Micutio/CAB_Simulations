"""
Main module of the urban development simulation.
This shall be used to experiment with growth models of cities or urban areas in
general.

Idea of v1.0:
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

from cab.cab_system import ComplexAutomaton

from abm.ud_agent import UrbanAgent
from ca.ud_cell import WorldCell
from ud_global_constants import GC
from util.ud_io_handling import EventHandler
from util.ud_visualization import Visualizer

__author__ = 'Michael Wagner'
__version__ = '1.0'


if __name__ == '__main__':

    gc = GC()
    pc = WorldCell(0, 0, gc)
    pa = UrbanAgent(0, 0, gc)
    ph = EventHandler(None)
    pv = Visualizer(gc, None, None)

    # Use assets to initialize simulation system.

    # simulation = ComplexAutomaton(gc, proto_cell=pc, proto_agent=pa, proto_handler=ph, proto_visualizer=pv)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)

    # Run the simulation
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
