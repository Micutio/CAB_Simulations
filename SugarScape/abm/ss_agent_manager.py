from abm.ss_agent import SSAgent

__author__ = 'Michael Wagner'
__version__ = '1.0'

import uuid
import math
import operator

from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_agent import CabAgent
from cab.ca.cab_ca_hex import CAHex
import cab.util.cab_rng

from abm.ss_genetics import Chromosome


class SSAgentManager(CabAgent):
    """
    This super agent acts as a manager of all Sugarscape agents.
    """
    def __init__(self, x, y, gc):
        super().__init__(None, None, gc)
        self.agent_counter = 0
        self.initial_run = True
        self.possible_starting_locations = []
        print('initialized agent manager')

    def perceive_and_act(self, abm, ca):
        if self.initial_run:
            self.agent_counter = len(abm.agent_set) - 1
            self.possible_starting_locations = list(ca.ca_grid.keys())
            while self.agent_counter < self.gc.START_AGENTS:
                # new_position = None
                # while new_position is None:
                #     temp_pos = ca.get_random_valid_position()
                #     if not (temp_pos in abm.agent_locations):
                #         new_position = temp_pos
                self.agent_counter += 1
                abm.add_agent(self.generate_agent(abm, ca))
            self.initial_run = False

    def generate_agent(self, abm, ca):
        # x, y = ca.get_random_valid_position()
        # while (x, y) in abm.agent_locations:
        #     x, y = ca.get_random_valid_position()
        x, y = get_RNG().choice(self.possible_starting_locations)
        self.possible_starting_locations.remove((x, y))
        meta_sugar = get_RNG().randint(self.gc.MIN_METABOLISM, self.gc.MAX_METABOLISM)
        meta_spice = get_RNG().randint(self.gc.MIN_METABOLISM, self.gc.MAX_METABOLISM)
        vision = get_RNG().randint(1, self.gc.VISION + 1)
        g = get_RNG().choice([0, 1])
        if g == 1:
            f1 = get_RNG().randint(self.gc.F_FERTILITY_START[0], self.gc.F_FERTILITY_START[1])
            f2 = get_RNG().randint(self.gc.F_FERTILITY_END[0], self.gc.F_FERTILITY_END[1])
            f = (f1, f2)
        else:
            f1 = get_RNG().randint(self.gc.M_FERTILITY_START[0], self.gc.M_FERTILITY_START[1])
            f2 = get_RNG().randint(self.gc.M_FERTILITY_END[0], self.gc.M_FERTILITY_END[1])
            f = (f1, f2)
        su = get_RNG().randint(self.gc.STARTING_SUGAR[0], self.gc.STARTING_SUGAR[1])
        sp = get_RNG().randint(self.gc.STARTING_SUGAR[0], self.gc.STARTING_SUGAR[1])
        d = get_RNG().randint(f[1], self.gc.MAX_AGENT_LIFE)
        c = [get_RNG().randint(0, int((meta_sugar + meta_spice) / 2)) for _ in range(11)]
        # imm_sys = [get_RNG().getrandbits(self.gc.NUM_TRIBES - 1) for _ in range(self.gc.IMMUNE_SYSTEM_GENOME_LENGTH)]
        imm_sys = [get_RNG().getrandbits(int((meta_sugar + meta_spice) / 2)) for _ in range(self.gc.IMMUNE_SYSTEM_GENOME_LENGTH)]
        a = 0  # get_RNG().randint(0, int(self.gc.MAX_AGENT_LIFE / 2))
        gene_string = "{0:03b}".format(meta_sugar) + "{0:03b}".format(meta_spice)\
                      + "{0:06b}".format(su) + "{0:06b}".format(sp) \
                      + "{0:03b}".format(vision) + "{0:01b}".format(g)\
                      + "{0:06b}".format(f[0]) + "{0:06b}".format(f[1]) + "{0:07b}".format(d)
        # We use generation to keep track of how far an agent has walked down the evolutionary road.
        generation = (0, 0)
        genome = (gene_string, gene_string, c, imm_sys, generation)

        # Retrieve a spawn position from the position list belonging to its tribe.
        # tribe_id = max(set(c), key=c.count)
        # get_RNG().shuffle(position_list[tribe_id])
        # p = position_list[tribe_id].pop()
        # Create the new agent and add to both, dictionary and list.
        new_agent = SSAgent(x, y, self.gc, su, sp, a, genome)
        # self.agent_dict[x, y] = new_agent
        # self.agent_list.append(new_agent)
        # abm.add_agent(new_agent)
        return new_agent
