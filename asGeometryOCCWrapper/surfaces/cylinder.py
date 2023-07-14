from OCC.Core.Geom import Geom_CylindricalSurface
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

from .base_surfaces import BaseElementarySurface

class Cylinder(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Cylinder'
    
    @staticmethod
    def getColor():
        return (0, 0, 255) #blue
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_CylindricalSurface(adaptor.Cylinder())
    
    @classmethod
    def _geomFromDict(cls, features: dict):
        geom = Geom_CylindricalSurface(cls._features2Ax3(features), features['radius'])
        return geom
    
    def getRadius(self):
        return self._geom.Radius()

    def toDict(self):   
        features = super().toDict()

        features['radius'] = self.getRadius()

        return features