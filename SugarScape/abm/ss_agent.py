__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid

import math
from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_agent import CabAgent

class SSAgent(CabAgent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.vision = gc.VISION
        

    def perceive_and_act(self, ca, abm):
        neighbors = ca.get_agent_neighborhood(abm.agent_locations, self.x, self.y, self.vision)
        best_cell = None
        for k, v in list(neighbors.items()):
            if best_cell == None:
                best_cell = v[0]
            elif v[0].sugar > best_cell.sugar and ( not v[1] or len(v[1]) < 1 ):
                best_cell = v[0]
        self.move_to(best_cell)


    def move_to(self, target_c):
        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = target_c.x
        self.y = target_c.y



class SSAgentManager(CabAgent):
    def __init__(self, x, y, gc):
        super().__init__(None, None, gc)
        self.agent_counter = 0

    def perceive_and_act(self, ca, abm):
        self.agent_counter = len(abm.agent_set) - 1
        while self.agent_counter < self.gc.START_AGENTS:
            self.agent_counter += 1
            abm.add_agent(self.generate_agent())

    def generate_agent(self):
        agnt_x = random.choice(range(5, self.gc.DIM_X - 5))
        agnt_y = random.choice(range(5, self.gc.DIM_Y - 5))
        return SSAgent(agnt_x, agnt_y, self.gc)