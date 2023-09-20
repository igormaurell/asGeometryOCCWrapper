import abc
from typing import Union

from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pnt2d, gp_Ax3
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCC.Core.GeomLib import geomlib_NormEstim
from OCC.Core.Geom import Geom_Surface

import numpy as np
import open3d as o3d

from ..geometry.base_geometry import BaseGeometry, angleDeviation, distanceDeviation
from ..curves import CurveFactory

class BaseSurface(BaseGeometry, metaclass=abc.ABCMeta):

    MESH_INFO_KEYS = BaseGeometry.MESH_INFO_KEYS + ['face_indices']

    @staticmethod
    @abc.abstractmethod
    def adaptor2Geom(adaptor: Union[BRepAdaptor_Surface, GeomAdaptor_Surface]):
        pass

    def __init__(self, geom: Geom_Surface, topods_orientation: int = 2):
        super().__init__(geom, topods_orientation=topods_orientation)

    def _getPointNormalParamFromProjector(self, projector, normal_tol=1e-3):
        try:
            proj_point = projector.NearestPoint().Coord()
        except:
            proj_point = (np.nan, np.nan, np.nan)

        try:
            u, v = projector.LowerDistanceParameters()
        except:
            u, v = np.nan, np.nan

        normal_gp = gp_Dir()
        r = geomlib_NormEstim(self._geom, gp_Pnt2d(u, v),  normal_tol, normal_gp)

        if r >= 2:
            normal = (np.nan, np.nan, np.nan)
        else:
            if self._orientation == 1:
                normal_gp.Reverse()
            normal = normal_gp.Coord()

        return proj_point, normal, (u, v)

    def projectPointsOnGeometry(self, points: list):
        proj_points = []
        proj_normals = []
        proj_params = []

        if isinstance(points, np.ndarray):
            points = points.tolist()

        if len(points) == 0:
            return [], [], []

        projector = GeomAPI_ProjectPointOnSurf()

        projector.Init(gp_Pnt(*points[0]), self._geom) 

        pt, nr, pr = self._getPointNormalParamFromProjector(projector)
        
        proj_points.append(pt)
        proj_normals.append(nr)
        proj_params.append(pr)

        for i in range(1, len(points)):
            projector.Perform(gp_Pnt(*(points[i])))

            pt, nr, pr = self._getPointNormalParamFromProjector(projector)
        
            proj_points.append(pt)
            proj_normals.append(nr)
            proj_params.append(pr)
                
        return np.asarray(proj_points), np.asarray(proj_normals), np.asarray(proj_params)
    
    def computeMeshNormals(self, normalized=True):
        self._mesh.compute_vertex_normals(normalized)
    
    def setMeshByGlobal(self, global_mesh: o3d.geometry.TriangleMesh, mesh_info: dict = None):
        res = super().setMeshByGlobal(global_mesh, mesh_info)

        if res == 0:
            return res
        
        if self._mesh_info is None or len(self._mesh_info['vert_indices']) == 0 or len(self._mesh_info['face_indices']) == 0:
            return 1
                
        vert_indices = np.asarray(self._mesh_info['vert_indices'], dtype=np.uint64)
        reverse_vert_map = dict([(vi, i) for i, vi in enumerate(vert_indices)])
        face_indices = np.asarray(self._mesh_info['face_indices'], dtype=np.uint64)
        faces_local = np.vectorize(reverse_vert_map.get)(np.asarray(global_mesh.triangles)[face_indices])

        self._mesh = o3d.geometry.TriangleMesh()
        self._mesh.vertices = o3d.utility.Vector3dVector(np.asarray(global_mesh.vertices)[vert_indices])
        self._mesh.triangles = o3d.utility.Vector3iVector(faces_local)
        #TODO: add if for the other possible data from global_mesh
    
        if not self._mesh.has_vertex_normals():
            self.computeMeshNormals()
        
        return 4
    
    def computeErrors(self, points, normals=None, params=None, symmetric_normals=False):
        p_points, p_normals, p_params = self.projectPointsOnGeometry(points)

        results = []

        distances = distanceDeviation(points, p_points)
        results.append(distances)

        if normals is not None:
            deviations = angleDeviation(normals, p_normals, symmetric=(symmetric_normals or self._orientation==2))
            results.append(deviations)

        return tuple(results)

    def validateMesh(self, dtol: float = 1e-6, atol: float = 10):
        if self._mesh_info is None or self._mesh is None:
            return False
        
        if not self._mesh.has_vertex_normals():
            self.computeMeshNormals()
        
        vertices = np.asarray(self._mesh.vertices)
        normals = np.asarray(self._mesh.vertex_normals)
        params = np.asarray(self._mesh_info['vert_parameters'])

        p_vertices, p_normals, p_params = self.projectPointsOnGeometry(self._mesh.vertices)

        distances = distanceDeviation(vertices, p_vertices)
        dist_erros = distances[distances > dtol]

        deviations = angleDeviation(normals, p_normals)
        dev_errors = deviations[deviations > atol]

        #ERROR
        ret = True
        if len(dist_erros) > 0:
            ret = False
            mean_error = float(np.mean(dist_erros))
            percent_error = (len(dist_erros)/len(distances))
            print(f'[ERROR] Vertices on {self.getType()}: error of {percent_error:.2%} and {mean_error:.8f} m')
        
        if len(dev_errors) > 0:
            ret = False
            mean_error = float(np.mean(dev_errors))
            percent_error = (len(dev_errors)/len(deviations))
            normals_with_error = np.hstack((normals[deviations > atol], p_normals[deviations > atol]))
            print(f'[ERROR] Normals on {self.getType()}: error of {percent_error:.2%} and {mean_error:.2f}° \n {normals_with_error}')
        
        return ret


class BaseElementarySurface(BaseSurface, metaclass=abc.ABCMeta):

    @staticmethod
    def _features2Ax3(features : dict):
        if 'x_axis' in features:
            return gp_Ax3(gp_Pnt(*features['location']),
                          gp_Dir(*features['z_axis']),
                          gp_Dir(*features['x_axis']))
        else:
            return gp_Ax3(gp_Pnt(*features['location']),
                          gp_Dir(*features['z_axis']))
    
    def getLocation(self):
        return self._geom.Position().Location().Coord()

    def getCoefficients(self):
        return list(self._geom.Coefficients())
    
    def getXAxis(self):
        return self._geom.Position().XDirection().Coord()

    def getYAxis(self):
        return self._geom.Position().YDirection().Coord()
    
    def getZAxis(self):
        return self._geom.Position().Direction().Coord()

    def toDict(self):       
        features = super().toDict()
                       
        features['location'] = self.getLocation()
        features['x_axis'] = self.getXAxis()
        features['y_axis'] = self.getYAxis()
        features['z_axis'] = self.getZAxis()
        features['coefficients'] = self.getCoefficients()
            
        return features

class BaseBoundedSurface(BaseSurface, metaclass=abc.ABCMeta):
 
    # def _fixOrientation(self):
    #     if self._orientation == 1:
    #         old_lower_bound = np.array(self.getLowerBound())
    #         old_upper_bound = np.array(self.getUpperBound())
    #         self._geom.UReverse()
    #         self._geom.VReverse()
    #         new_lower_bound = np.array(self.getLowerBound())
    #         new_upper_bound = np.array(self.getUpperBound())
            
    #         assert np.all(np.isclose(old_lower_bound, new_upper_bound)) and \
    #                np.all(np.isclose(old_upper_bound, new_lower_bound)), \
    #                f'Sanity Check Failed: problem in reversing a {self.getType()}. ' \
    #                f'\n\t\t~~~~~ {old_lower_bound} != {new_upper_bound} or' \
    #                f'{old_upper_bound} != {np.flip(new_lower_bound)} ~~~~~'
        
    def getLowerBound(self):
        return tuple(self._geom.Bounds()[2:])

    def getUpperBound(self):
        return tuple(self._geom.Bounds()[:2])

    def toDict(self):
        features = super().toDict()
            
        return features
    
class BaseSweptSurface(BaseSurface, metaclass=abc.ABCMeta):
         
    # def _fixOrientation(self):
    #     pass

    def getCurve(self):
        return CurveFactory.fromGeom(self._geom.BasisCurve(), 
                                     topods_orientation=self._orientation)

    def toDict(self):
        features = super().toDict()

        features['curve'] = self.getCurve().toDict()
            
        return features