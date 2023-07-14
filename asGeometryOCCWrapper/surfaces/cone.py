from OCC.Core.Geom import Geom_ConicalSurface
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

from .base_surfaces import BaseElementarySurface

class Cone(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Cone'
    
    @staticmethod
    def getColor():
        return (0, 255, 0) #green
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_ConicalSurface(adaptor.Cone())

    @classmethod
    def _geomFromDict(cls, features: dict):
        geom = Geom_ConicalSurface(cls._features2Ax3(features), features['angle'], features['radius'])
        return geom

    def getRadius(self):
        return self._geom.RefRadius()
    
    def getSemiAngle(self):
        return self._geom.SemiAngle()
    
    def getApex(self):
        return self._geom.Apex().Coord()
    
    def toDict(self):   
        features = super().toDict()

        features['radius'] = self.getRadius()
        features['angle'] = self.getSemiAngle()
        features['apex'] = self.getApex()

        return features