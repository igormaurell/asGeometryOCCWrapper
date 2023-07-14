from OCC.Core.Geom import Geom_SphericalSurface
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

import numpy as np

from .base_surfaces import BaseElementarySurface

class Sphere(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Sphere'
    
    @staticmethod
    def getColor():
        return (255, 255, 0) #yellow
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_SphericalSurface(adaptor.Sphere())
    
    @classmethod
    def _geomFromDict(cls, features: dict):
        geom = Geom_SphericalSurface(cls._features2Ax3(features), features['radius'])
        return geom
    
    def getRadius(self):
        return self._geom.Radius()

    def toDict(self):   
        features = super().toDict()

        features['radius'] = self.getRadius()

        return features