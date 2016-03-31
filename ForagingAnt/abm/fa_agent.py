__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid
import math

from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_agent import CabAgent


class HiveAgent(CabAgent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.id = "hive"
        self.max_ants = gc.MAX_ANTS
        self.food = 0
        self.dead = False
        self.spawned = 0
        

    def perceive_and_act(self, ca, abm):
        if self.spawned < self.max_ants:
            ant = AntAgent(self.x, self.y, self.gc)
            abm.add_agent(ant)
            self.spawned += 1

    def clone(self):
        return HiveAgent(x, y, gc)


class FoodAgent(CabAgent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.id = "food"
        self.food = gc.MAX_FOOD
        self.dead = False

    def perceive_and_act(self, ca, agent_list):
        if self.food < 0:
            self.dead = True
        return


class AntAgent(CabAgent):
    def __init__(self, x, y, gc):
        """
        Initializes an agent
        """
        super().__init__(x, y, gc)
        self.id = "ant"
        self.prev_x = x
        self.prev_y = y
        self.max_ph = gc.MAX_PHEROMONE
        self.food = 1
        self.has_food = False
        self.dead = False
        self.directions = [(1,  0), (1, -1), ( 0, -1), (-1,  0), (-1, 1), ( 0, 1)]
        self.current_dir = random.randint(0, 5)

    def perceive_and_act(self, ca, abm):
        """
        Perceiving the environment and act according to the rules
        """
        self.prev_x = self.x
        self.prev_y = self.y
        neighborhood = ca.get_agent_neighborhood(abm.agent_locations, self.x, self.y, 1)

        self.forage(neighborhood)

    def forage(self, neighborhood):
        if self.has_food:
            self.return_to_hive(neighborhood)
        else:
            self.find_food_source(neighborhood)

    def return_to_hive(self, neighborhood):
        cell = self.get_cell_with_pheromone("hive", neighborhood)
        if cell:
            this_cell = neighborhood[self.x, self.y]
            self.drop_pheromones("food", this_cell)
            self.move_to(cell[0])
            self.check_if_at_hive(cell[1])
        else:
            print('Ant Error: no valid hive bound cell found!')

    def find_food_source(self, neighborhood):
        cell = self.get_cell_with_pheromone("food", neighborhood)
        if cell:
            this_cell = neighborhood[self.x, self.y]
            self.drop_pheromones("hive", this_cell)
            self.move_to(cell[0])
            self.check_if_at_food(cell[1])
        else:
            print('Ant Error: no valid hive bound cell found!')

    def get_cell_with_pheromone(self, target_ph, neighborhood):
        """
        Gets the cell with highest pheromone value (or random if no pheromones present)
        from the immediate neighborhood.
        :param: neighborhood is a dict of (x, y) -> cell mappings,
        where cell is a tuple of (ca_cell, [agent(s) on cell]).
        If no agent is on the cell then the list in the tuple is simply 'False'
        """
        result = None
        result_list = []
        backup_list = []
        best_cell = None
        max_ph = 0

        # Choose the possible directions the ants can currently look at.
        if self.current_dir == 5:
            possible_dirs = [4, 5, 0]
        elif self.current_dir == 0:
            possible_dirs = [5, 0, 1]
        else:
            possible_dirs = [self.current_dir -1, self.current_dir, self.current_dir + 1]

        for i in possible_dirs:
            d = self.directions[i]
            _x = self.x + d[0]
            _y = self.y + d[1]
            if (_x, _y) in neighborhood:
                cell = neighborhood[_x, _y]
                if cell[0].pheromones[target_ph] > 0:  # and (not cell[1] or len(cell[1]) < 10):
                    ph = cell[0].pheromones[target_ph]
                    if ph > max_ph:
                        best_cell = cell
                        max_ph = ph
                        self.current_dir = i
                    result_list.append((cell, ph, i))
                # elif not cell[1] or len(cell[1]) < 10:
                else:
                    backup_list.append((cell, i))
        if result_list:
            if random.random() < 0.01:
                choice = weighted_choice(result_list)
                result = choice[0]
                self.current_dir = choice[1]
            else:
                result = best_cell
        elif backup_list:
            choice = random.choice(backup_list)
            result = choice[0]
            self.current_dir = choice[1]
        else:
            # print('Ant Error: no cells found to move to!')
            self.current_dir = get_opposite_direction(self.current_dir)
            return self.get_cell_with_pheromone(target_ph, neighborhood)
        return result

    def drop_pheromones(self, target_ph, cell):
        if cell[1]:
            for agent in cell[1]:
                # Check if one of the agents present on this cell is hive or food.
                if agent.id == target_ph:
                    cell[0].pheromones[target_ph] = self.max_ph
                    return

        max_ph = cell[0].last_neighbor_max_pheromone[target_ph]
        des = max_ph - 2
        d = des - cell[0].pheromones[target_ph]
        if d > 0:
            cell[0].pheromones[target_ph] += d
        return

    def move_to(self, target_c):
        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = target_c.x
        self.y = target_c.y

    def check_if_at_hive(self, agents_at_cell):
        if agents_at_cell:
            for agent in agents_at_cell:
                if agent.id == "hive":
                    # print('found the hive!')
                    agent.food += self.food
                    self.has_food = False

    def check_if_at_food(self, agents_at_cell):
        if agents_at_cell:
            for agent in agents_at_cell:
                if agent.id == "food":
                    # print('found the food!')
                    agent.food -= self.food
                    self.has_food = True


def weighted_choice(choices):
    total = sum(w for c, w, i in choices)
    r = random.uniform(0, total)
    up_to = 0
    for c, w, i in choices:
        if up_to + w > r:
            return c, i
        up_to += w
    assert False, "Shouldn't get here"

def get_opposite_direction(number):
    if number < 3:
        return number + 3
    else:
        return number - 3