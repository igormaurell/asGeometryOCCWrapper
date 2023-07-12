from OCC.Core.Geom import Geom_SphericalSurface
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

import numpy as np

from .base_surfaces import BaseElementarySurface

class Sphere(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Sphere'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_SphericalSurface(adaptor.Sphere())
    
    @classmethod
    def fromDict(cls, features: dict):
        geom = Geom_SphericalSurface(gp_Ax3(gp_Pnt(*features['location']), 
                                              gp_Dir(*features['z_axis']),
                                              gp_Dir(*features['x_axis'])), features['radius'])
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    def getRadius(self):
        return self._geom.Radius()

    def toDict(self):   
        features = super().toDict()

        features['radius'] = self.getRadius()

        return features