# Author: Rodrigo Loza
# Description: This script contains functions that interact with the microscope's hardware 
# and the focus coefficients received from the sensor 

from interface import *

class autofocus:
    def __init__(self, list = [(None, None)]):
        self.positions = [each for each in list]
	self.coefficients = [each[1] for each in list]

    def focus(self):
        # Calculate the maximum value 
	max_ = max(self.coefficients)
	pos = self.positions.index(max_)
        # Go back to the desired position
	for i in range( 10-pos ):
            z(500, 0, 500)
