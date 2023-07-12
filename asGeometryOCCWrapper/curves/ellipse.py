from OCC.Core.Geom import Geom_Ellipse
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir

from .base_curves import BaseConicCurve

class Ellipse(BaseConicCurve):

    @staticmethod
    def getType():
        return 'Ellipse'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_Ellipse(adaptor.Ellipse())
    
    @classmethod
    def _fromDict(cls, features: dict):
        geom = Geom_Ellipse(gp_Ax2(gp_Pnt(*features['location']), gp_Dir(*features['z_axis']),
                                   gp_Dir(*features['x_axis'])), features['x_radius'], features['y_radius'])
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    def getFocus1(self):
        return self._geom.Focus1().Coord()
    
    def getFocus2(self):
        return self._geom.Focus2().Coord()
    
    def getMinorRadius(self):
        return self._geom.MinorRadius()
    
    def getMajorRadius(self):
        return self._geom.MajorRadius()

    def toDict(self):        
        features = super().toDict()
        
        features['focus1'] = self.getFocus1()
        features['focus2'] = self.getFocus2()
        features['x_radius'] = self.getMajorRadius()
        features['y_radius'] = self.getMinorRadius()

        return features