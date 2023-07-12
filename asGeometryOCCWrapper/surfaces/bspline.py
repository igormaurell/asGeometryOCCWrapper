from OCC.Core.Geom import Geom_BSplineSurface
from OCC.Core.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal, TColStd_Array2OfReal
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.gp import gp_Pnt

from .base_surfaces import BaseBoundedSurface

from asGeometryOCCWrapper.utils import list2tcol1d, list2tcol2d

class BSpline(BaseBoundedSurface):

    @staticmethod
    def getType():
        return 'BSpline'
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return adaptor.BSpline()
    
    @classmethod
    def fromDict(cls, features: dict):
        poles = list2tcol2d(features['poles'], TColgp_Array2OfPnt, gp_Pnt)
        u_knots = list2tcol1d(features['u_knots'], TColStd_Array1OfReal, float)
        v_knots = list2tcol1d(features['v_knots'], TColStd_Array1OfReal, float)
        weights = list2tcol2d(features['weights'], TColStd_Array2OfReal, float)
        u_multiplicities = list2tcol1d(features['u_multiplicities'], TColStd_Array1OfInteger, int)
        v_multiplicities = list2tcol1d(features['v_multiplicities'], TColStd_Array1OfInteger, int)
        geom = Geom_BSplineSurface(poles, weights, u_knots, v_knots, u_multiplicities, v_multiplicities,
                                   features['u_degree'], features['v_degree'], features['u_periodic'], features['v_periodic'])
        orientation = int(not features['foward'])
        return cls(geom, orientation)
    
    def getIsURational(self):
        return self._geom.IsURational()

    def getIsVRational(self):
        return self._geom.IsVRational()
    
    def getIsVPeriodic(self):
        return self._geom.IsVPeriodic()

    def getIsUPeriodic(self):
        return self._geom.IsUPeriodic()
    
    def getIsUClosed(self):
        return self._geom.IsUClosed()
    
    def getIsVClosed(self):
        return self._geom.IsVClosed()
    
    def getContinuity(self):
        return self._geom.Continuity()
    
    def getUDegree(self):
        return self._geom.UDegree()
    
    def getVDegree(self):
        return self._geom.VDegree()
    
    def getPoles(self):
        data = TColgp_Array2OfPnt(1, self._geom.NbUPoles(), 1, self._geom.NbVPoles())
        self._geom.Poles(data)
        return [list(list(data.Value(i+1, j+1).Coord()) for j in range(data.RowLength()))
                for i in range(data.ColLength())]

    def getUKnots(self):
        data = TColStd_Array1OfReal(1, self._geom.NbUKnots())
        self._geom.UKnots(data)
        return list(data)

    def getVKnots(self):
        data = TColStd_Array1OfReal(1, self._geom.NbVKnots())
        self._geom.VKnots(data)
        return list(data)

    def getWeights(self):
        data = TColStd_Array2OfReal(1, self._geom.NbUPoles(), 1, self._geom.NbVPoles())
        self._geom.Weights(data)
        print(data.RowLength(), data.ColLength())
        return [list(data.Value(i+1, j+1) for j in range(data.RowLength())) 
                for i in range(data.ColLength())]

    def getUMultiplicities(self):
        data = TColStd_Array1OfInteger(1, self._geom.NbUKnots())
        self._geom.UMultiplicities(data)
        return list(data)

    def getVMultiplicities(self):
        data = TColStd_Array1OfInteger(1, self._geom.NbVKnots())
        self._geom.VMultiplicities(data)
        return list(data)
        
    def toDict(self):
        features = super().toDict()
        
        features['u_rational'] = self.getIsURational()
        features['v_rational'] = self.getIsVRational()
        features['u_periodic'] = self.getIsUPeriodic()
        features['v_periodic'] = self.getIsVPeriodic()
        features['u_closed'] = self.getIsUClosed()
        features['v_closed'] = self.getIsVClosed()
        features['continuity'] = self.getContinuity()
        features['u_degree'] = self.getUDegree()
        features['v_degree'] = self.getVDegree()
        features['poles'] = self.getPoles()
        features['u_knots'] = self.getUKnots()
        features['v_knots'] = self.getVKnots()
        features['weights'] = self.getWeights()
        features['u_multiplicities'] = self.getUMultiplicities()
        features['v_multiplicities'] = self.getVMultiplicities()

        return features