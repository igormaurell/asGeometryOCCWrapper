from OCC.Core.Geom import Geom_ToroidalSurface
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

from .base_surfaces import BaseElementarySurface

class Torus(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Torus'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_ToroidalSurface(adaptor.Torus())

    @classmethod
    def fromDict(cls, features: dict):
        geom = Geom_ToroidalSurface(gp_Ax3(gp_Pnt(*features['location']), 
                                           gp_Dir(*features['z_axis']),
                                           gp_Dir(*features['x_axis'])),
                                           features['max_radius'], features['min_radius'])
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    #TODO: add coeffs to torus
    def getCoefficients(self):    
        return []
    
    def getMajorRadius(self):    
        return self._geom.MajorRadius()
    
    def getMinorRadius(self):    
        return self._geom.MinorRadius()

    def toDict(self):
        features = super().toDict()

        features['max_radius'] = self.getMajorRadius()
        features['min_radius'] = self.getMinorRadius()

        return features