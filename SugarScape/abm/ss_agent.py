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
        

    def perceive_and_act(self, ca, abm):
        pass

    def clone(self):
        return SSAgent(x, y, gc)
