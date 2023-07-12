from OCC.Core.Geom import Geom_CylindricalSurface
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

from .base_surfaces import BaseElementarySurface

class Cylinder(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Cylinder'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_CylindricalSurface(adaptor.Cylinder())
    
    @classmethod
    def _fromDict(cls, features: dict):
        geom = Geom_CylindricalSurface(gp_Ax3(gp_Pnt(*features['location']), 
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