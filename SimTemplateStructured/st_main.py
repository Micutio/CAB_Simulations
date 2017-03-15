"""
Main module of the foraging ant simulation.
"""

# Import the Complex Automaton simulation system.
from cab.cab_system import ComplexAutomaton

# Import all customized simulation components.
from st_global_constants import ExampleGC
from ca.st_cell import ExampleCell
from abm.st_agent import ExampleAgent
from util.st_io_handling import ExampleEventHandler
from util.st_visualization import ExampleVisualizer


__author__ = 'Michael Wagner'
__version__ = '1.0'


if __name__ == '__main__':
    """
    Main method of the simulation: get up and running in three steps.
    """

    # 1. initialize all components
    gc = ExampleGC()
    pc = ExampleCell(0, 0, gc)
    pa = ExampleAgent(0, 0, gc)
    ph = ExampleEventHandler(None)
    pv = ExampleVisualizer(gc, None, None)

    # 2. initialize the complex automaton system with the components
    simulation = ComplexAutomaton(gc, proto_agent=pa, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)

    # 3. run the complex automaton system
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
