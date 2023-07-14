from OCC.Core.Geom import Geom_Circle
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir

from .base_curves import BaseConicCurve

class Circle(BaseConicCurve):

    @staticmethod
    def getType():
        return 'Circle'
    
    @staticmethod
    def getColor():
        return (255, 0, 128) #pink

    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_Circle(adaptor.Circle())
    
    @classmethod
    def _geomFromDict(cls, features: dict):
        geom = Geom_Circle(cls._features2Ax2(features), features['radius'])
        return geom
    
    def getRadius(self):
        return self._geom.Radius()

    def toDict(self):        
        features = super().toDict()
        
        features['radius'] = self.getRadius()

        return features