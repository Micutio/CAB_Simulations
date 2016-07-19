__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid
import math
import operator

from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_agent import CabAgent
from cab.ca.cab_ca_hex import CAHex

from abm.ss_agent_manager import AgentManager
from abm.ss_genetics import Chromosome

class SSAgent(CabAgent):
    def __init__(self, x, y, gc, su, sp, age, genomes):
        super().__init__(x, y, gc)
        self.vision = gc.VISION
        self.sugar = su
        self.spice = sp
        self.age = age
        self.chromosome = Chromosome(genomes)
        self.init_sugar = self.chromosome.init_sugar
        self.init_spice = self.chromosome.init_spice
        self.meta_sugar = self.chromosome.meta_sugar
        self.meta_spice = self.chromosome.meta_spice
        self.vision = self.chromosome.vision
        self.gender = self.chromosome.gender
        self.fertility = self.chromosome.fertility
        self.dying_age = self.chromosome.dying_age
        self.culture = self.chromosome.culture
        self.sugar_gathered = 0
        self.spice_gathered = 0
        self.sugar_traded = 0
        self.spice_traded = 0
        self.sugar_price = 0
        self.spice_price = 0
        self.children = []
        self.diseases = {}
        self.immune_system = ["".join(map(str, self.chromosome.immune_system))]

    def perceive_and_act(self, ca, abm):
        best_cell = self.r1_select_best_cell(ca, abm)
        self.move_to(best_cell)
        self.eat_from(best_cell)

    def r1_select_best_cell(self, ca, abm):
        """
        Agent selects the best cell to move to, according to: its resources, occupier and tribal alignment.
        """
        neighborhood = ca.get_empty_agent_neighborhood(abm.agent_locations, self.x, self.y, self.vision)
        best_cells = list()
        max_dist = 0
        max_w = 0

        # Find cells with the highest possible reward.
        # TODO: check if distance calculation is correct for hex grids
        for cell in list(neighborhood.values()):
            if not best_cells:
                best_cells = [cell]
                max_w = self.welfare(cell.sugar, cell.spice)
                max_dist = (abs(cell.x - self.x) + abs(cell.y - self.y))
            else:
                dist = (abs(cell.x - self.x) + abs(cell.y - self.y))
                dist = ca.hex_distance(self.x, self.y, cell.q, cell.r)
                welfare = self.welfare(cell.sugar, cell.spice)
                if welfare > max_w:
                    best_cells = [cell]
                    max_w = welfare
                    max_dist = dist
                elif welfare == max_w and dist < max_dist:
                    best_cells = [cell]
                    max_dist = dist
                elif welfare == max_w and dist == max_dist:
                    best_cells.append(cell)
        result_cell = random.choice(best_cells)
        # if self.vision > 1:
        #     _q, _r = CAHex.get_cell_in_direction(ca.ca_grid[self.x, self.y], result_cell)
        #     return ca.ca_grid[_q, _r]
        # else:
        return result_cell

    def welfare(self, su, sp):
        """
        Welfare function a.k.a. Cobb-Douglas form.
        Relates the time the agent will die of lack of sugar with
        the time the agent will die of lack of spice.
        :param su: potential sugar gain of cell in question.
        :param sp: potential spice gain of cell in question.
        :return: welfare value, important to calculate prices in the trading rule.
        """
        gain_sugar = max(self.sugar + su, 0)
        gain_spice = max(self.spice + sp, 0)
        meta_total = self.meta_sugar + self.meta_spice
        w1 = math.pow(gain_sugar, (self.meta_sugar / meta_total))
        w2 = math.pow(gain_spice, (self.meta_spice / meta_total))
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
        self.sugar += cell.sugar
        self.spice += cell.spice
        cell.sugar = 0
        cell.spice = 0
        self.sugar -= self.meta_sugar
        self.spice -= self.meta_spice

    def r2_procreate(self, ca, abm):
        neighborhood = ca.get_agent_neighborhood(abm.agent_locations, self.x, self.y, 1)

        if self.is_fertile():
            free_cells = [v[0] for v in list(neighborhood.values()) if v[1] is None]
            mates = [v[1] for v in list(neighborhood.values()) if not v[1] is None]

            if mates:
                m = random.choice(mates)
                both_wealthy1 = (self.sugar >= self.init_sugar and m.sugar >= m.init_sugar)
                both_wealthy2 = (self.spice >= self.init_spice and m.spice >= m.init_spice)
                # All criteria is fulfilled to procreate!
                if free_cells and m.is_fertile() and m.gender != self.gender and both_wealthy1 and both_wealthy2:
                    # Take one free cell to place Junior there.
                    c = random.choice(free_cells)
                    n_x = c.x
                    n_y = c.y
                    n_s = self.size
                    # Give him / her initial resources
                    n_su = int(self.init_sugar / 2) + int(m.init_sugar / 2)
                    n_sp = int(self.init_spice / 2) + int(m.init_spice / 2)
                    self.sugar -= int(self.init_sugar / 2)
                    self.spice -= int(self.init_spice / 2)
                    m.sugar -= int(m.init_sugar / 2)
                    m.spice -= int(m.init_spice / 2)
                    # Fuse mommy's and daddy's chromosomes to create Juniors attributes.
                    # This is the actual creation of the baby. Behold the wonders of nature!
                    n_chromosome = self.chromosome.merge_with(m.chromosome)
                    child = Agent(n_x, n_y, n_s, n_su, n_sp, n_chromosome, 0, self.tribe)
                    # Give the parents a reference to their newborn so they can,
                    # inherit their wealth to it before their inevitable demise.
                    self.children.append(child)
                    m.children.append(child)
                    # Update the abm that it has to schedule a new agent.
                    abm.add_agent(child)
                    return child

    def r3_trading(self, ca, abm):
        """
        Trade with neighboring agents if possible.
        """
        trade_count = 0
        self.sugar_price = 0
        self.spice_price = 0
        for n in neighbors:
            if not n[1]is None and not n[1].dead and not self.dead and n[1].sugar > 0 and n[1].spice > 0:
                m1_now = self.mrs(0, 0)
                m2_now = n[1].mrs(0, 0)
                mrs_diff = m1_now - m2_now
                while mrs_diff != 0:
                    # Calculate welfare.
                    w1_now = self.welfare(0, 0)
                    w2_now = n[1].welfare(0, 0)
                    # Set directions of traded resources
                    if mrs_diff < 0:
                        sugar_flow = -1
                        spice_flow = 1
                        direction = False
                    else:  # m1 < m2
                        sugar_flow = 1
                        spice_flow = -1
                        direction = True
                    # Calculate exchange price p as geometric mean.
                    price = math.sqrt(m1_now * m2_now)
                    if price > 1:  # Trade p units of spice for 1 sugar.
                        my_sugar_delta = int(sugar_flow * 1)
                        my_spice_delta = int(spice_flow * int(price))
                        neigh_sugar_delta = int(my_sugar_delta * -1)
                        neigh_spice_delta = int(my_spice_delta * -1)
                    else:  # p < 1, Trade 1/p units of sugar for 1 spice.
                        my_sugar_delta = int(sugar_flow * int(1 / price))
                        my_spice_delta = int(spice_flow * 1)
                        neigh_sugar_delta = int(my_sugar_delta * -1)
                        neigh_spice_delta = int(my_spice_delta * -1)
                    # Trade only if welfare of both agents increases.
                    # Trade only if neither agent loses resources.
                    my_trade_valid = self.sugar + my_sugar_delta > 0 and self.spice + my_spice_delta > 0
                    neigh_trade_valid = n[1].sugar + neigh_sugar_delta > 0 and n[1].spice + neigh_spice_delta > 0
                    if my_trade_valid and neigh_trade_valid:
                        w1_expected = self.welfare(my_sugar_delta, my_spice_delta)
                        w2_expected = n[1].welfare(neigh_sugar_delta, neigh_spice_delta)
                        if w1_expected > w1_now and w2_expected > w2_now:
                            # Trade only if mrs values of agents are not flipping.
                            # (If mrs flips, they would infinitely trade their goods back and forth.)
                            m1_expected = self.mrs(my_sugar_delta, my_spice_delta)
                            m2_expected = n[1].mrs(neigh_sugar_delta, neigh_spice_delta)
                            mrs_diff = m1_expected - m2_expected
                            if (mrs_diff > 0 and direction) or (mrs_diff < 0 and not direction):
                                self.sugar += my_sugar_delta
                                self.spice += my_spice_delta
                                n[1].sugar += neigh_sugar_delta
                                n[1].spice += neigh_spice_delta
                                # Gather information for the trading statistics.
                                # 1.) general trading stats
                                self.sugar_traded += abs(my_sugar_delta)
                                self.spice_traded += abs(my_spice_delta)
                                self.sugar_price += abs(price)
                                self.spice_price += abs(1 / price)
                                trade_count += 1
                                # 2.) wealth change between tribes, if occurred
                                if self.tribe_id != n[1].tribe_id:
                                    my_wealth_change = my_sugar_delta + my_spice_delta
                                    neigh_wealth_change = neigh_spice_delta + neigh_sugar_delta
                                    self.tribe.tribal_wealth[self.tribe_id] += my_wealth_change
                                    self.tribe.tribal_wealth[n[1].tribe_id] += neigh_wealth_change
                            else:
                                mrs_diff = 0
                        else:
                            mrs_diff = 0
                    else:
                        mrs_diff = 0
        # Finish up trading and save possibly gathered data.
        if trade_count > 0:
            self.sugar_price /= trade_count
            self.spice_price /= trade_count

    def r4_diseases(self, neighbors):
        """
        All diseases, the agent is currently infected with, are trying to spread to its neighbors.
        """
        #for n in neighbors:
        #    if n[1] and not n[1].dead and not self.dead:
        #        for _, d in self.diseases.items():
        #            d.spread(n[1])
        for _, d in self.diseases.items():
            targets = [agent for (cell, agent) in neighbors if not agent is None and not agent.dead and not self.dead]
            if targets:
                victim = random.choice(targets)
                d.spread(victim)

        # Let the immune system build another instance
        # and then attempt to fight the diseases.
        self.im_create_antibodies()
        self.immune_reaction()
        # Reset the metabolism values of the agent to clear all past diseases.
        # That way, the diseases just fought off by the immune system are not longer
        # afflicting the body and possible new diseases can act on the agent.
        self.meta_sugar = self.chromosome.meta_sugar
        self.meta_spice = self.chromosome.meta_spice
        # Have the diseases affect the agent
        for _, d in self.diseases.items():
            d.affect(self)

    def im_create_antibodies(self):
        if self.fertility[0] < self.age < self.fertility[1] and len(self.immune_system) <= 10:
            is_copy = copy.deepcopy(self.chromosome.immune_system)
            length = len(is_copy)
            index = random.choice(range(length))
            is_copy[index] = 1 - is_copy[index]
            self.immune_system.append("".join(map(str, is_copy)))

    def immune_reaction(self):
        eliminated = set()
        for _, d in self.diseases.items():
            for i in self.immune_system:
                # If the immune system has one instance that fits
                # into the disease genome, the agent is now
                # successfully healed from it and immune to future infections.
                if i in d.genome_string:
                    eliminated.add(d.genome_string)
        # Remove all eliminated diseases from our agent dictionary
        for d in eliminated:
            del(self.diseases[d])

    def die(self, agent_positions):
        """
        As the name suggests, this method is to be executed upon the agent's death.
        """
        # Remove myself from the world
        del(agent_positions[self.x, self.y])
        self.dead = True
        # Inherit my wealth to all my kids
        if self.children:
            num_kids = len(self.children)
            for c in self.children:
                c.sugar += math.floor(self.sugar / num_kids)
                c.spice += math.floor(self.spice / num_kids)

        # Update tribe's information
        self.tribe.tribal_wealth[self.tribe_id] -= (self.sugar + self.spice)
        self.sugar = 0
        self.spice = 0

