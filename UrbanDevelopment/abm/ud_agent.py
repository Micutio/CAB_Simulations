

from cab.abm.cab_agent import CabAgent

__author__ = 'Michael Wagner'
__version__ = '1.0'


class UrbanAgent(CabAgent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.id = "UrbanAgent"

    def perceive_and_act(self, ca, abm):
        pass
