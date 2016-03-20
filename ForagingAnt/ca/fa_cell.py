"""
Module containing the cell definition for the ant world.
"""

from cab.cab_global_constants import GlobalConstants
from cab.ca.cab_cell import CellHex

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
        #self.neighbor_pheromones = {"hive": 0, "food": 0}
        #self.num_neighbors = 0
        self.num_neighbors = 0
        self.neighbor_pheromones = {"hive": 0, "food": 0}
        self.neighbor_max_pheromone = {"hive": 0, "food": 0}
        self.last_neighbor_max_pheromone = {"hive": 0, "food": 0}


    def clone(self, x, y, gc):
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