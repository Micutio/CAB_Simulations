"""
Module containing the cell definition for the urban world.
"""

from cab.ca.cab_cell import CellHex

__author__ = 'Michael Wagner'
__version__ = '1.0'


class WorldCell(CellHex):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.zone = EmptyZone()

    def clone(self, x, y):
        return WorldCell(x, y, self.gc)

    def sense_neighborhood(self):
        self.num_neighbors = 0
        for n in self.neighbors:
            self.num_neighbors += 1

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass

class EmptyZone():
    """
    This class residential zones.
    """
    def __init__(self):
        self.type = "EMPTY"
        self.color = (0, 0, 0)

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass


class ResidentialZone():
    """
    This class residential zones.
    """
    def __init__(self):
        self.type = "RESIDENTIAL"
        self.color = (0, 255 , 0)

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass


class CommercialZone():
    """
    This class commercial zones.
    """
    def __init__(self):
        self.type = "COMMERCIAL"
        self.color = (0, 0, 255)

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass


class IndustrialZone():
    """
    This class industrial zones.
    """
    def __init__(self, x, y, gc):
        self.type = "INDUSTRIAL"
        self.color = (0, 255 , 255)

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass
