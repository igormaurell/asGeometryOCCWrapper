from OCC.Core.Geom import Geom_Line
from OCC.Core.gp import gp_Pnt, gp_Dir

from .base_curves import BaseCurve

class Line(BaseCurve):
    
    @staticmethod
    def getType():
        return 'Line'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_Line(adaptor.Line())
    
    @classmethod
    def _fromDict(cls, features: dict):
        geom = Geom_Line(gp_Pnt(*features['location']), gp_Dir(*features['direction']))
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    def getLocation(self):
        return self._geom.Position().Location().Coord()
    
    def getDirection(self):
        return self._geom.Position().Direction().Coord()

    def toDict(self):
        features = super().toDict()
                       
        features['location'] = self.getLocation()
        features['direction'] = self.getDirection()
            
        return features