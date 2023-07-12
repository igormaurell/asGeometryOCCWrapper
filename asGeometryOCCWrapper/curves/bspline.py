from OCC.Core.Geom import Geom_BSplineCurve
from OCC.Core.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt

from .base_curves import BaseBoundedCurve

from asGeometryOCCWrapper.utils import list2tcol1d

class BSpline(BaseBoundedCurve):

    @staticmethod
    def getType():
        return 'BSpline'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return adaptor.BSpline()
    
    @classmethod
    def fromDict(cls, features: dict):
        poles = list2tcol1d(features['poles'], TColgp_Array1OfPnt, gp_Pnt)
        knots = list2tcol1d(features['knots'], TColStd_Array1OfReal, float)
        weights = list2tcol1d(features['weights'], TColStd_Array1OfReal, float)
        multiplicities = list2tcol1d(features['multiplicities'], TColStd_Array1OfInteger, int)
        geom = Geom_BSplineCurve(poles, weights, knots, multiplicities, 
                                 features['degree'], features['periodic'])
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    def getIsRational(self):
        return self._geom.IsRational()
    
    def getIsPeriodic(self):
        return self._geom.IsPeriodic()
    
    def getIsClosed(self):
        return self._geom.IsClosed()
    
    def getContinuity(self):
        return self._geom.Continuity()
    
    def getDegree(self):
        return self._geom.Degree()
    
    def getPoles(self):
        data = TColgp_Array1OfPnt(1, self._geom.NbPoles())
        self._geom.Poles(data)
        return [list(pole.Coord()) for pole in data]

    def getKnots(self):
        data = TColStd_Array1OfReal(1, self._geom.NbKnots())
        self._geom.Knots(data)
        return list(data)

    def getWeights(self):
        data = TColStd_Array1OfReal(1, self._geom.NbPoles())
        self._geom.Weights(data)
        return list(data)
    
    def getMultiplicities(self):
        data = TColStd_Array1OfInteger(1, self._geom.NbKnots())
        self._geom.Multiplicities(data)
        return list(data)

    def toDict(self):        
        features = super().toDict()
        
        features['rational'] = self.getIsRational()
        features['periodic'] = self.getIsPeriodic()
        features['closed'] = self.getIsClosed()
        features['continuity'] = self.getContinuity()
        features['degree'] = self.getDegree()
        features['poles'] = self.getPoles()
        features['knots'] = self.getKnots()
        features['weights'] = self.getWeights()
        features['multiplicities'] = self.getMultiplicities()

        return features