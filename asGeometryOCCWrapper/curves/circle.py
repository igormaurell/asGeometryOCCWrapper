from OCC.Core.Geom import Geom_Circle
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir

from .base_curves import BaseConicCurve

class Circle(BaseConicCurve):

    @staticmethod
    def getType():
        return 'Circle'

    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_Circle(adaptor.Circle())
    
    @classmethod
    def fromDict(cls, features: dict):
        geom = Geom_Circle(gp_Ax2(gp_Pnt(*features['location']), gp_Dir(*features['z_axis']),
                                  gp_Dir(*features['x_axis'])), features['radius'])
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    def getRadius(self):
        return self._geom.Radius()

    def toDict(self):        
        features = super().toDict()
        
        features['radius'] = self.getRadius()

        return features