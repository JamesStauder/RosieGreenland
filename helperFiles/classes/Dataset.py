from pylab import sqrt, linspace
from scipy.interpolate import RectBivariateSpline

from ..createColorMaps import *

import numpy as np

'''
Class: Dataset
Argument list: name of dataset, pen type(used for plotting)
Purpose: This is the class of datasets. This will store velocity, smb, etc. This takes the Velocity in X and Y direction
and makes one dataset of just Velocity. This velocity dataset ONLY stores the magnitude but not direction.

Dependencies: pylabs sqrt and linspace, RectBivariateSplint, numpy
Creator: James Stauder
Date created:2/23/18
Last edited: 3/2/18
'''


class Dataset:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.interp = RectBivariateSpline(map['y'], map['x'], data)

        # Only create color map if we wish to render possible in the future where we wish to create
        # Dataset for backend web
        if name != 'VX' and name != 'VY':
            createColorMap(self)

    def getInterpolatedValue(self, xPosition, yPosition):
        return self.interp(yPosition, xPosition)
