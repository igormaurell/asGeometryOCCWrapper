from typing import Union
import abc

from OCC.Core.Geom import Geom_Curve
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2

import numpy as np
import open3d as o3d

from ..geometry.base_geometry import BaseGeometry

class BaseCurve(BaseGeometry, metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def adaptor2Geom(adaptor: Union[BRepAdaptor_Curve, GeomAdaptor_Curve]):
        pass

    def __init__(self, geom: Geom_Curve , topods_orientation: int = 0):
        super().__init__(geom, topods_orientation=topods_orientation)

    def _fixOrientation(self):
        if self._orientation == 1:
            self._geom.Reverse()

    def projectPointsOnGeometry(self, points):
        return [], [], []

    def setMeshByGlobal(self, global_mesh: o3d.geometry.LineSet, mesh_info: dict = None):
        res = super().setMeshByGlobal(global_mesh, mesh_info)

        if res == 0:
            return res
        
        if self._mesh_info is None or len(self._mesh_info['vert_indices']) == 0:
            return 1
                
        vert_indices = np.asarray(self._mesh_info['vert_indices'], dtype=np.uint64)

        self._mesh = o3d.geometry.LineSet()
        self._mesh.points = o3d.utility.Vector3dVector(np.asarray(global_mesh.vertices)[vert_indices])
        lines = np.asarray([[i, i+1] for i in range(len(self._mesh.points) - 1)])
        self._mesh.lines = o3d.utility.Vector2iVector(lines)
        #TODO: add if for the other possible data from global_mesh
    
        return 4


class BaseConicCurve(BaseCurve, metaclass=abc.ABCMeta):

    @staticmethod
    def _features2Ax2(features : dict):
        if 'x_axis' in features:
            return gp_Ax2(gp_Pnt(*features['location']),
                          gp_Dir(*features['z_axis']),
                          gp_Dir(*features['x_axis']))
        else:
            return gp_Ax2(gp_Pnt(*features['location']),
                          gp_Dir(*features['z_axis']))
    
    def getLocation(self):
        return self._geom.Location().Coord()
    
    def getXAxis(self):
        return self._geom.XAxis().Direction().Coord()

    def getYAxis(self):
        return self._geom.YAxis().Direction().Coord()
    
    def getZAxis(self):
        return self._geom.Axis().Direction().Coord()
        
    def toDict(self):       
        features = super().toDict()
                       
        features['location'] = self.getLocation()
        features['x_axis'] = self.getXAxis()
        features['y_axis'] = self.getYAxis()
        features['z_axis'] = self.getZAxis()
            
        return features

class BaseBoundedCurve(BaseCurve, metaclass=abc.ABCMeta):
                
    def getStartPoint(self):
        return self._geom.StartPoint().Coord()
    
    def getEndPoint(self):
        return self._geom.EndPoint().Coord()