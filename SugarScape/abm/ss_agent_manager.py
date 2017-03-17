from abm.ss_agent import SSAgent

__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid
import math
import operator

from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_agent import CabAgent
from cab.ca.cab_ca_hex import CAHex

from abm.ss_genetics import Chromosome


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
            new_position = None
            while new_position is None:
                temp_pos = ca.get_random_valid_position()
                if not (temp_pos in abm.agent_locations):
                    new_position = temp_pos
                    self.agent_counter += 1
                    abm.add_agent(self.generate_agent(ca, abm))

    def generate_agent(self, ca, abm):
        x = 0
        y = 0
        while (x, y) in abm.agent_locations:
            x = random.randint(0, self.gc.DIM_X)
            y = random.randint(0, self.gc.DIM_Y)
        meta_sugar = random.randint(self.gc.MIN_METABOLISM, self.gc.MAX_METABOLISM)
        meta_spice = random.randint(self.gc.MIN_METABOLISM, self.gc.MAX_METABOLISM)
        vision = random.randint(1, self.gc.VISION + 1)
        g = random.choice([0, 1])
        if g == 1:
            f1 = random.randint(self.gc.F_FERTILITY_START[0], self.gc.F_FERTILITY_START[1])
            f2 = random.randint(self.gc.F_FERTILITY_END[0], self.gc.F_FERTILITY_END[1])
            f = (f1, f2)
        else:
            f1 = random.randint(self.gc.M_FERTILITY_START[0], self.gc.M_FERTILITY_START[1])
            f2 = random.randint(self.gc.M_FERTILITY_END[0], self.gc.M_FERTILITY_END[1])
            f = (f1, f2)
        su = random.randint(self.gc.STARTING_SUGAR[0], self.gc.STARTING_SUGAR[1])
        sp = random.randint(self.gc.STARTING_SUGAR[0], self.gc.STARTING_SUGAR[1])
        d = random.randint(f[1], self.gc.MAX_AGENT_LIFE)
        c = [random.randint(0, int((meta_sugar + meta_spice) / 2)) for _ in range(11)]
        # imm_sys = [random.getrandbits(self.gc.NUM_TRIBES - 1) for _ in range(self.gc.IMMUNE_SYSTEM_GENOME_LENGTH)]
        imm_sys = [random.getrandbits(int((meta_sugar + meta_spice) / 2)) for _ in range(self.gc.IMMUNE_SYSTEM_GENOME_LENGTH)]
        a = 0  # random.randint(0, int(self.gc.MAX_AGENT_LIFE / 2))
        gene_string = "{0:03b}".format(meta_sugar) + "{0:03b}".format(meta_spice)\
                      + "{0:06b}".format(su) + "{0:06b}".format(sp) \
                      + "{0:03b}".format(vision) + "{0:01b}".format(g)\
                      + "{0:06b}".format(f[0]) + "{0:06b}".format(f[1]) + "{0:07b}".format(d)
        # We use generation to keep track of how far an agent has walked down the evolutionary road.
        generation = (0, 0)
        genome = (gene_string, gene_string, c, imm_sys, generation)

        # Retrieve a spawn position from the position list belonging to its tribe.
        # tribe_id = max(set(c), key=c.count)
        # random.shuffle(position_list[tribe_id])
        # p = position_list[tribe_id].pop()
        # Create the new agent and add to both, dictionary and list.
        new_agent = SSAgent(x, y, self.gc, su, sp, a, genome)
        # self.agent_dict[x, y] = new_agent
        # self.agent_list.append(new_agent)
        abm.add_agent(new_agent)
        return new_agent
