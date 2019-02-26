"""
Insert a module description
"""

import random
from cab.abm.agent import CabAgent


__author__ = 'Michael Wagner'
__version__ = '1.0'


class CreeplingAgent(CabAgent):
    """
    Derive the new agent class from the CabAgent to let the CAB System know how to handle it.
    """
    def __init__(self, x, y, gc, team, min_density, strategy_walk, strategy_seed, power):
        super().__init__(x, y, gc)
        self.team = team
        self.min_density = min_density
        self.strategy_walk = strategy_walk  # 0 - random, 1 - min-based
        self.strategy_seed = strategy_seed  # 0 - random, 1 - min-based
        self.score = 0
        self.power = power
        
    def perceive_and_act(self, abm, ca):
        """
        This method is called at every simulation step, as long as this agent is alive.
        It can access the abm and ca to retrieve information about its surroundings.
        Make use of if to implement the agent's behavior.
        :param abm: Instance of the agent based model.
        :param ca: Instance of the cellular automaton.
        """
        neighborhood = ca.get_agent_neighborhood(self.x, self.y, 1)
        
        if self.strategy_walk == 0:
            random.shuffle(possible_cells)
            cell = random.choice(possible_cells)
        else:  # self.strategy_walk == 1:
            min_val = min(possible_cells, key=attrgetter('temperature'))
            c_list = [c for c in possible_cells if c.temperature == min_val.temperature]
            random.shuffle(c_list)
            cell = random.choice(c_list)


    # This is the minimum configuration for an agent. It does not need more than
    # to implement the perceive_and_act method from CabAgent to perform actions
    # in the simulation.
    #
    # There are additional methods designed for interacting with simulation components
    # via user input, which can be redefined just like init and perceive and act.
    
    def on_lmb_click(self, abm, ca):
        """
        Executed when the mouse is pointed at the agent and left mouse button clicked.
        """
        pass

    def on_rmb_click(self, abm, ca):
        """
        Executed when the mouse is pointed at the agent and right mouse button clicked.
        """
        pass

    def on_mouse_scroll_up(self, abm, ca):
        """
        Executed when the mouse is pointed at the agent and wheel scrolled up.
        """
        pass

    def on_mouse_scroll_down(self, abm, ca):
        """
        Executed when the mouse is pointed at the agent and wheel scrolled down.
        """
        pass
