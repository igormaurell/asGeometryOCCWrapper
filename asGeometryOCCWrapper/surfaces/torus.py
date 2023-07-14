from OCC.Core.Geom import Geom_ToroidalSurface
from OCC.Core.TColStd import TColStd_Array1OfReal
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

from .base_surfaces import BaseElementarySurface

class Torus(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Torus'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_ToroidalSurface(adaptor.Torus())
    
    @staticmethod
    def getColor():
        return (255, 0, 255) #magenta

    @classmethod
    def _geomFromDict(cls, features: dict):
        geom = Geom_ToroidalSurface(cls._features2Ax3(features), features['max_radius'], features['min_radius'])
        return geom
    
    def getCoefficients(self):
        data = TColStd_Array1OfReal(1, 31)
        try:
            self._geom.Coefficients(data)
        except:
            data = []
        return list(data)
    
    def getMajorRadius(self):    
        return self._geom.MajorRadius()
    
    def getMinorRadius(self):    
        return self._geom.MinorRadius()

    def toDict(self):
        features = super().toDict()

        features['max_radius'] = self.getMajorRadius()
        features['min_radius'] = self.getMinorRadius()

        return features