__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid
import math
import operator

from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_agent import CabAgent


class SSAgentManager(CabAgent):
    """
    This super agent acts as a manager of all Sugarscape agents.
    As the Sugarscape is 
    """
    def __init__(self, x, y, gc):
        super().__init__(None, None, gc)
        self.agent_counter = 0

    def perceive_and_act(self, ca, abm):
        self.agent_counter = len(abm.agent_set) - 1
        while self.agent_counter < self.gc.START_AGENTS:
            self.agent_counter += 1
            abm.add_agent(self.generate_agent(ca, abm))

    def generate_agent(self, ca, abm):
        new_position = None
        while new_position == None:
            temp_pos = ca.get_random_valid_position()
            if not (temp_pos in abm.agent_locations):
                new_position = temp_pos
        return SSAgent(new_position[0], new_position[1], self.gc)


class SSAgent(CabAgent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.vision = gc.VISION
        self.meta_sugar = gc.METABOLISM_SUGAR
        self.meta_spice = gc.METABOLISM_spice

    def perceive_and_act(self, ca, abm):
        best_cell = self.select_best_cell(ca, abm)
        self.move_to(best_cell)
        self.eat_from(best_cell)

    def select_best_cell(self, ca, abm):
        """
        Agent selects the best cell to move to, according to: its resources, occupier and tribal alignment.
        """
        neighborhood = ca.get_agent_neighborhood(abm.agent_locations, self.x, self.y, self.vision)
        best_cells = list()
        max_dist = 0
        max_w = 0

        # Find cells with the highest possible reward.
        # TODO: check if distance calculation is correct for hex grids
        for v in list(neighborhood.values()):
            if not best_cells:
                best_cells = [v[0]]
                max_w = self.welfare(v[0].sugar + occupant_sugar, v[0].spice + occupant_spice)
                max_dist = (abs(v[0].x - self.x) + abs(v[0].y - self.y))
            else:
                dist = (abs(v[0].x - self.x) + abs(v[0].y - self.y))
                welfare = self.welfare(v[0].sugar, v[0].spice)
                if welfare > max_w:
                    best_cells = [v]
                    max_w = welfare
                    max_dist = dist
                elif welfare == max_w and dist < max_dist:
                    best_cells = [v]
                    max_dist = dist
                elif welfare == max_w and dist == max_dist:
                    best_cells.append(v)

        return random.choice(best_cells)

    def welfare(self, su, sp):
        """
        Welfare function a.k.a. Cobb-Douglas form.
        Relates the time the agent will die of lack of sugar with
        the time the agent will die of lack of spice.
        :param su: potential sugar gain of cell in question.
        :param sp: potential spice gain of cell in question.
        :return: welfare value, important to calculate prices in the trading rule.
        """
        meta_total = self.meta_sugar + self.meta_spice
        w1 = math.pow((self.sugar + su), (self.meta_sugar / meta_total))
        w2 = math.pow((self.spice + sp), (self.meta_spice / meta_total))
        return w1 * w2

    def mrs(self, su, sp):
        """
        Marginal Rate of Substitution.
        Second important trading tool after welfare.
        MRS is used to calculate sugar and spice prices between two agents.
        :param su:
        :param sp:
        :return:
        """
        rate_sugar = (self.sugar + su) / self.meta_sugar
        rate_spice = (self.spice + sp) / self.meta_spice
        return rate_spice / rate_sugar

    def move_to(self, target_c):
        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = target_c.x
        self.y = target_c.y

    def eat_from(self, cell):
        cell.sugar = 0