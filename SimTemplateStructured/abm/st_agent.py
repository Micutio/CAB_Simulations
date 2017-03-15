"""
Insert a module description
"""

from cab.abm.cab_agent import CabAgent


__author__ = 'Michael Wagner'
__version__ = '1.0'


class ExampleAgent(CabAgent):
    """
    Derive the new agent class from the CabAgent to let the CAB System know how to handle it.
    """
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        # Calling the super method initializes the following attributes,
        # which every class that inherits CabAgent can make use of:
        # self.a_id = uuid.uuid4().urn
        # self.x = x
        # self.y = y
        # self.prev_x = x
        # self.prev_y = y
        # self.size = gc.CELL_SIZE
        # self.gc = gc
        # self.dead = False
        
    def perceive_and_act(self, abm, ca):
        """
        This method is called at every simulation step, as long as this agent is alive.
        It can access the abm and ca to retrieve information about its surroundings.
        Make use of if to implement the agent's behavior.
        :param abm: Instance of the agent based model.
        :param ca: Instance of the cellular automaton.
        """
        pass

    # This is the minimum configuration for an agent. It does not need more than
    # to implement the perceive_and_act method from CabAgent to perform actions
    # in the simulation.
