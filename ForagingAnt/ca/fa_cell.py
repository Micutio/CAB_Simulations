"""
Module containing the cell definition for the ant world.
"""

from cab.ca.cell import CellHex

from abm.fa_agent import HiveAgent, FoodAgent

__author__ = 'Michael Wagner'
__version__ = '1.0'


class WorldCell(CellHex):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.diffusion = gc.DIFFUSION
        self.evaporation = gc.EVAPORATION
        self.max_ph = gc.MAX_PHEROMONE
        self.pheromones = {"hive": 0, "food": 0}
        # self.neighbor_pheromones = {"hive": 0, "food": 0}
        # self.num_neighbors = 0
        self.num_neighbors = 0
        self.neighbor_pheromones = {"hive": 0, "food": 0}
        self.neighbor_max_pheromone = {"hive": 0, "food": 0}
        self.last_neighbor_max_pheromone = {"hive": 0, "food": 0}

    def clone(self, x, y):
        return WorldCell(x, y, self.gc)

    def sense_neighborhood(self):
        for n in self.neighbors:
            self.num_neighbors += 1
            for ph in ["hive", "food"]:
                self.neighbor_pheromones[ph] += n.pheromones[ph]
                if n.pheromones[ph] > self.neighbor_max_pheromone[ph]:
                    self.neighbor_max_pheromone[ph] = n.pheromones[ph]

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        for ph in ["hive", "food"]:
            avg = self.neighbor_pheromones[ph] / self.num_neighbors
            self.pheromones[ph] = (1.0 - self.evaporation) * (self.pheromones[ph] + self.diffusion * (avg - self.pheromones[ph]))
            if self.pheromones[ph] < self.evaporation:
                self.pheromones[ph] = 0

        self.num_neighbors = 0
        self.neighbor_pheromones = {"hive": 0, "food": 0}
        self.last_neighbor_max_pheromone = self.neighbor_max_pheromone
        self.neighbor_max_pheromone = {"hive": 0, "food": 0}

        green = 42 + int(213 * (self.pheromones["hive"] / self.gc.MAX_PHEROMONE))
        blue = 48 + int(207 * (self.pheromones["food"] / self.gc.MAX_PHEROMONE))
        red = 34  # + int((green + blue) / 2)
        self.color = (green, blue, red)

    def on_lmb_click(self, abm, ca):
        abm.add_agent(HiveAgent(self.x, self.y, self.gc))
        abm.schedule_new_agents()

    def on_rmb_click(self, abm, ca):
        abm.add_agent(FoodAgent(self.x, self.y, self.gc))
        abm.schedule_new_agents()