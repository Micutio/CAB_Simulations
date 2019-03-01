"""
Main module of the foraging ant simulation.
"""

# CAB system imports.
from cab.complex_automaton import ComplexAutomaton
import cab.util.logging as cab_log

# Internal Simulation System component imports.
from cw_global_constants import CreepWarsGC
from ca.cw_cell import CreepCell
from abm.cw_agent import CreepMasterAgent


__author__ = 'Michael Wagner'
__version__ = '1.0'


if __name__ == '__main__':
    """
    Main method of the simulation: get up and running in three steps.
    """
    cab_log.set_log_trace()

    # 1. initialize all components
    gc = CreepWarsGC()
    pc = CreepCell(0, 0, gc)
    pa = CreepMasterAgent(None, None, gc)

    # 2. initialize the complex automaton system with the components
    simulation = ComplexAutomaton(gc, proto_agent=pa, proto_cell=pc)

    # 3. run the complex automaton system
    simulation.run_main_loop()

    # If need be, the simulation can be run in profiling mode too!
    # cProfile.run("simulation.run_main_loop()")
