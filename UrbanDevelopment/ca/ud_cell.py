"""
Module containing the cell definition for the urban world.
"""

from cab.ca.cab_cell import CellHex

from cab.util.cab_rng import get_RNG

__author__ = 'Michael Wagner'
__version__ = '1.0'


class WorldCell(CellHex):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.zone = EmptyZone()
        self.neighbor_zones = set()

    def clone(self, x, y):
        return WorldCell(x, y, self.gc)

    def sense_neighborhood(self):
        if self.zone.type == 'EMPTY':
            for n in self.neighbors:
                if n.zone.type == "RESIDENTIAL":
                    self.neighbor_zones.add("INDUSTRIAL")
                elif n.zone.type == "COMMERCIAL":
                    self.neighbor_zones.add("RESIDENTIAL")
                elif n.zone.type == "INDUSTRIAL":
                    self.neighbor_zones.add("COMMERCIAL")
        else:
            self.zone.sense_neighborhood(self)

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        if self.zone == 'EMPTY':
            self.zone.update(self)
        else:
            if len(self.neighbor_zones) > 0:
                new_zone = get_RNG().choice(list(self.neighbor_zones))
                if new_zone == 'RESIDENTIAL':
                    self.zone = ResidentialZone()
                elif new_zone == 'COMMERCIAL':
                    self.zone = CommercialZone()
                elif new_zone == 'INDUSTRIAL':
                    self.zone = IndustrialZone()
                self.color = self.zone.color
        self.neighbor_zones.clear()

    def on_lmb_click(self, abm, ca):
        """
        On left mouse click, cycle through zones.
        """
        if self.zone.type == "EMPTY":
            self.zone = ResidentialZone()
        elif self.zone.type == 'RESIDENTIAL':
            self.zone = CommercialZone()
        elif self.zone.type == 'COMMERCIAL':
            self.zone = IndustrialZone()
        elif self.zone.type == 'INDUSTRIAL':
            self.zone = EmptyZone()
        self.color = self.zone.color

class EmptyZone():
    """
    This class represents empty zones.
    """
    def __init__(self):
        self.type = "EMPTY"
        self.color = (0, 0, 0)

    def sense_neighborhood(self, parent_cell):
        pass

    def update(self, parent_cell):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass


class ResidentialZone():
    """
    This class represents residential zones.
    """
    def __init__(self):
        self.type = "RESIDENTIAL"
        self.color = (0, 255 , 0)

    def sense_neighborhood(self, parent_cell):
        pass

    def update(self, parent_cell):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass


class CommercialZone():
    """
    This class represents commercial zones.
    """
    def __init__(self):
        self.type = "COMMERCIAL"
        self.color = (0, 0, 255)

    def sense_neighborhood(self, parent_cell):
        pass

    def update(self, parent_cell):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass


class IndustrialZone():
    """
    This class represents industrial zones.
    """
    def __init__(self):
        self.type = "INDUSTRIAL"
        self.color = (255, 255 , 0)

    def sense_neighborhood(self, parent_cell):
        pass

    def update(self, parent_cell):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass
