"""
Insert a module description
"""

import math
from operator import attrgetter

from cab.abm.agent import CabAgent
import cab.util.rng as cab_rng


__author__ = 'Michael Wagner'
__version__ = '1.0'


class Team:
    def __init__(self, number, color, walk, seed):
        self.number = number
        self.color = color
        self.strategy_walk = walk
        self.strategy_seed = seed


class CreeplingAgent(CabAgent):
    """
    Creeplings that walk around the landscape, spreading the creep of their team.
    """

    def __init__(self, x, y, gc, team, min_density, power):
        super().__init__(x, y, gc)
        self.min_density = min_density
        self.strategy_walk = cab_rng.get_RNG().randint(0, 1)  # team.strategy_walk  # 0 - random, 1 - min-based
        self.strategy_seed = cab_rng.get_RNG().randint(0, 1)  # team.strategy_seed  # 0 - random, 1 - min-based
        self.score = 0
        self.power = power
        self.color = team.color
        self.team = team

    def perceive_and_act(self, abm, ca):
        """
        This method is called at every simulation step, as long as this agent is alive.
        It can access the abm and ca to retrieve information about its surroundings.
        Make use of if to implement the agent's behavior.
        :param abm: Instance of the agent based model.
        :param ca: Instance of the cellular automaton.
        """
        neighborhood = ca.get_empty_agent_neighborhood(self.x, self.y, 1)
        self.walk(neighborhood)
        self.spread_creep(neighborhood)

    def walk(self, neighborhood):
        possible_cells = [c for c in list(neighborhood.values(
        )) if c.team and self.team.number == c.team.number and c.temperature >= self.min_density]
        self.prev_x = self.x
        self.prev_y = self.y
        if possible_cells:
            if self.strategy_walk == 0:
                cab_rng.get_RNG().shuffle(possible_cells)
                cell = cab_rng.get_RNG().choice(possible_cells)
            else:  # self.strategy_walk == 1:
                min_val = min(possible_cells, key=attrgetter('temperature'))
                c_list = [c for c in possible_cells if c.temperature ==
                          min_val.temperature]
                cab_rng.get_RNG().shuffle(c_list)
                cell = cab_rng.get_RNG().choice(c_list)
            # Move to new cell

            self.x = cell.x
            self.y = cell.y
        else:
            print("agent died: t{0} d{1} w{2} s{3} p{4}".format(
                self.team.number, self.min_density, self.strategy_seed, self.strategy_seed, self.power))
            self.dead = True

    def spread_creep(self, neighborhood):
        cells = [c for c in list(neighborhood.values())]
        possible_cells = [
            c for c in cells if c.team and self.team.number == c.team.number]
        if possible_cells:
            if self.strategy_seed == 0:
                cab_rng.get_RNG().shuffle(cells)
                cell = cab_rng.get_RNG().choice(cells)
            else:
                min_val = min(possible_cells, key=attrgetter('temperature'))
                c_list = [c for c in possible_cells if c.temperature ==
                          min_val.temperature]
                c_list.extend(
                    [c for c in cells if not c.team or self.team.number != c.team.number])
                cab_rng.get_RNG().shuffle(c_list)
                cell = cab_rng.get_RNG().choice(c_list)
            self.score += cell.inc_temperature(self.team, self.power)
        else:
            print("agent died: t{0} d{1} w{2} s{3} p{4}".format(
                self.team.number, self.min_density, self.strategy_seed, self.strategy_seed, self.power))
            self.dead = True


class CreepHive(CabAgent):
    """
    Stationary hive, spawning creeplings
    """

    def __init__(self, x, y, gc, team):
        super().__init__(x, y, gc)
        self.team = team
        self.color = team.color
        self.size = 10
        self.max_creeplings = 50
        self.current_creeplings = 0
        self.has_spawned_creepling_this_turn = False
        # TODO: Implement more strategies and rules for creepling generation

    def perceive_and_act(self, abm, ca):
        self.has_spawned_creepling_this_turn = False
        neighborhood = ca.get_empty_agent_neighborhood(self.x, self.y, 1)
        possible_cells = list(neighborhood.values())
        for c in possible_cells:
            if not c.team or c.team.number != self.team.number:
                self.dead = True
                break
            if self.current_creeplings < self.max_creeplings and not self.has_spawned_creepling_this_turn:
                density = cab_rng.get_RNG().randint(1, 15)
                power = cab_rng.get_RNG().randint(1, 10)
                abm.add_agent(CreeplingAgent(
                    c.x, c.y, self.gc, self.team, density, power))
                self.current_creeplings += 1
                self.has_spawned_creepling_this_turn = True


class CreepMasterAgent(CabAgent):
    """
    Spawn hives and assign the cells around them to their teams.
    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.teams = list()
        self.has_spawned_hives = False
        self.create_teams()
        # TODO: Re-implement 'Thermal Creep' scenario-specific mechanics from abm.

    def perceive_and_act(self, abm, ca):
        if not self.has_spawned_hives:
            self.create_hives_symmetrical(abm, ca)
            self.has_spawned_hives = True

    def create_teams(self):
        self.teams = [
            Team(1, (200, 30, 30), 0, 0),
            Team(2, (200, 200, 30), 1, 0),
            Team(3, (30, 200, 30), 0, 1),
            Team(4, (60, 60, 200), 1, 1)
        ]

    def create_hives_symmetrical(self, abm, ca):
        # Get coordinates that are roughly symmetrically distributed in the CA.
        x_min = 0 - math.floor(0 / 2)
        y_min = 0
        x_max = self.gc.DIM_X - math.floor(self.gc.DIM_Y / 2)
        y_max = self.gc.DIM_Y

        x_quart = (x_max - x_min) / 4
        y_quart = (y_max - y_min) / 4

        abm.add_agent(CreepHive(int(x_min + x_quart), int(y_min +
                                                          y_quart), self.gc, self.teams[0]))
        for c in list(ca.get_cell_neighborhood(int(x_min + x_quart), int(y_min + y_quart), 1).values()):
            c.team = self.teams[0]
            c.temperature = 100

        abm.add_agent(CreepHive(int(x_max - x_quart), int(y_min +
                                                          y_quart), self.gc, self.teams[1]))
        for c in list(ca.get_cell_neighborhood(int(x_max - x_quart), int(y_min + y_quart), 1).values()):
            c.team = self.teams[1]
            c.temperature = 100

        abm.add_agent(CreepHive(int(x_min + x_quart), int(y_max -
                                                          y_quart), self.gc, self.teams[2]))
        for c in list(ca.get_cell_neighborhood(int(x_min + x_quart), int(y_max - y_quart), 1).values()):
            c.team = self.teams[2]
            c.temperature = 100

        abm.add_agent(CreepHive(int(x_max - x_quart), int(y_max -
                                                          y_quart), self.gc, self.teams[3]))
        for c in list(ca.get_cell_neighborhood(int(x_max - x_quart), int(y_max - y_quart), 1).values()):
            c.team = self.teams[3]
            c.temperature = 100

        # for team in self.teams:
        #     # TODO: get x and y coordinates
        #     abm.add(CreepHive(x, y, gc, team))
