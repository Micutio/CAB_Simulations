"""
Insert a module description
"""

import random
from operator import attrgetter

from cab.abm.agent import CabAgent


__author__ = 'Michael Wagner'
__version__ = '1.0'

class Team:
    def __init__(self, number, color):
        self.number = number
        self.color = color

class CreeplingAgent(CabAgent):
    """
    Creeplings that walk around the landscape, spreading the creep of their team.
    """
    def __init__(self, x, y, gc, team, min_density, strategy_walk, strategy_seed, power):
        super().__init__(x, y, gc)
        self.min_density = min_density
        self.strategy_walk = strategy_walk  # 0 - random, 1 - min-based
        self.strategy_seed = strategy_seed  # 0 - random, 1 - min-based
        self.score = 0
        self.power = power
        self.color = team.color   
        self.team = team.number
        
    def perceive_and_act(self, abm, ca):
        """
        This method is called at every simulation step, as long as this agent is alive.
        It can access the abm and ca to retrieve information about its surroundings.
        Make use of if to implement the agent's behavior.
        :param abm: Instance of the agent based model.
        :param ca: Instance of the cellular automaton.
        """
        neighborhood = ca.get_empty_agent_neighborhood(self.x, self.y, 1)
        possible_cells = [c for c in list(neighborhood.values()) if self.team == c.team and c.temperature >= self.min_density]
        
        if possible_cells:
            if self.strategy_walk == 0:
                random.shuffle(possible_cells)
                cell = random.choice(possible_cells)
            else:  # self.strategy_walk == 1:
                min_val = min(possible_cells, key=attrgetter('temperature'))
                c_list = [c for c in possible_cells if c.temperature == min_val.temperature]
                random.shuffle(c_list)
                cell = random.choice(c_list)
            # Move to new cell
            self.x = cell.x
            self.y = cell.y
            cell.inc_temperature(self.team, self.power)
            self.score += cell.inc_temperature(self.team, self.power)
        else:
            self.dead = True

class CreepHive(CabAgent):
    """
    Stationary hive, spawning creeplings
    """
    def __init__(self, x, y, gc, team):
        super().__init__(x, y, gc)
        self.team = team
        self.size = 10

    def perceive_and_act(self, abm, ca):
        neighborhood = ca.get_empty_agent_neighborhood(self.x, self.y, 1)
        possible_cells = list(neighborhood.values())
        for c in possible_cells:
            if c.team != self.team.number:
                self.dead = true
                break;

class MasterAgent(CabAgent):
    """
    Spawn hives and assign the cells around them to their teams.
    """
    def __init(self, None, None, gc):
        pass
        # TODO: Re-implement 'Thermal Creep' scenario-specific mechanics from abm.