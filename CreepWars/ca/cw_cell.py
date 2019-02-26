"""
Module containing the Creep cell definition.
"""

# Internal library imports.
from cab.ca.cell import CellHex

__author__ = 'Michael Wagner'
__version__ = '1.0'


class CreepCell(CellHex):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    It inherits from the class CellHex because we declared in the global constants class that this project
    is working with a Cellular Automaton that uses hexagonal cells.
    If instead one wants to use rectangular cells, then CreepCell has to inherit from CellRect.
    """

    def __init__(self, x, y, gc):
        """
        Initializer method. Usually a cell only needs to know their individual coordinates
        and a reference to the class containing all globally declared constants.
        :param x: X-position of the cell.
        :param y: Y-position of the cell.
        :param gc: Reference to the class containing global constants.
        """
        super().__init__(x, y, gc)
        self.temperature = 0
        self.team = -1
        self.decay = 0

    def clone(self, x, y):
        """
        The clone method has to be implemented to let the cellular automaton know how to create
        more instances of CreepCell to fill the grid up with cells.
        :param x: X-position of the cell.
        :param y: Y-position of the cell.
        :return: A new instance of the same class, CreepCell.
        """
        return CreepCell(x, y, self.gc)

    def sense_neighborhood(self):
        """
        This method is called at each simulation step to let the cell acquire information about
        its neighboring cells. With this information the cell can then decide whether to change
        its own state. The actual state change however has to be performed within the update()
        method.
        """
        # Creep: iterate over all neighboring cells and get information from them.
        # for n in self.neighbors:
        #   do some thing with neighbor n
        pass

    def update(self):
        """
        This method is called at each simulation step, following the sense_neighborhood() method
        to let the cell make changes to its current state. If The information gathered ("sensed")
        in the method sense_neighborhood() warrants any change of this cell's state, then it will
        be performed in this update method, right now.
        """
        if self.decay == 100:
            if self.temperature > 0:
                self.temperature -= 1
            else:
                self.team = -1
            self.decay = 0
        else:
            self.decay += 1

    def increase_temperature(self, team, power):
        """
        Called by agents on the cell to raise the temperature of their own team.
        """
        result = 0
        if self.team == team:
            if (self.temperature + power) < self.gc.MAX_TEMPERATURE:
                self.temperature += power
                result = power
        else:
            self.temperature -= power
            result = power
            if self.temperature <= 0:
                self.team = team
                self.temperature = 0
        return result

    def update_color(self):
        c = int(255 * (self.temperature / self.gc.MAX_TEMPERATURE))
        if self.team == 0:
            col = (c, 0, 0)
        elif self.team == 1:
            col = (c, c, 0)
        elif self.team == 2:
            col = (0, c, 0)
        else:
            col = (0, 0, c)
        return col
