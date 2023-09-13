from typing import Union

from OCC.Core.GeomAbs import GeomAbs_SurfaceType
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface
from OCC.Core.Geom import Geom_Surface

from .cone import Cone
from .plane import Plane
from .torus import Torus
from .sphere import Sphere
from .cylinder import Cylinder
from .bspline import BSpline
from .extrusion import Extrusion
from .revolution import Revolution

#TODO: make a GeometryFactory class for Curve and Surface
class SurfaceFactory:

    FEATURES_SURFACE_CLASSES = {
        'Plane': Plane,
        'Cylinder': Cylinder,
        'Cone': Cone,
        'Sphere': Sphere,
        'Torus': Torus,
        'BSpline': BSpline,
        #GeomAbs_SurfaceType.GeomAbs_SurfaceOfExtrusion: Extrusion,
        #GeomAbs_SurfaceType.GeomAbs_SurfaceOfRevolution: Revolution
    }

    OCC_SURFACE_CLASSES = {
        GeomAbs_SurfaceType.GeomAbs_Plane: Plane,
        GeomAbs_SurfaceType.GeomAbs_Cylinder: Cylinder,
        GeomAbs_SurfaceType.GeomAbs_Cone: Cone,
        GeomAbs_SurfaceType.GeomAbs_Sphere: Sphere,
        GeomAbs_SurfaceType.GeomAbs_Torus: Torus,
        GeomAbs_SurfaceType.GeomAbs_BSplineSurface: BSpline,
        #GeomAbs_SurfaceType.GeomAbs_SurfaceOfExtrusion: Extrusion,
        #GeomAbs_SurfaceType.GeomAbs_SurfaceOfRevolution: Revolution
    }
        
    @classmethod
    def adaptor2Geom(cls, adaptor: Union[BRepAdaptor_Surface, GeomAdaptor_Surface]):
        cls_type = GeomAbs_SurfaceType(adaptor.GetType())
        if cls_type in cls.OCC_SURFACE_CLASSES:
            geom = cls.OCC_SURFACE_CLASSES[cls_type].adaptor2Geom(adaptor)
            return geom, cls_type

    @classmethod
    def fromTopoDS(cls, topods: TopoDS_Face):
        brep_adaptor = BRepAdaptor_Surface(topods)
        return cls.fromAdaptor(brep_adaptor, topods_orientation=topods.Orientation())
        
    @classmethod
    def fromAdaptor(cls, adaptor: Union[BRepAdaptor_Surface, GeomAdaptor_Surface], topods_orientation: int = 2):
        r = cls.adaptor2Geom(adaptor)
        if r is not None:
            return cls.fromGeom(r[0], topods_orientation=topods_orientation, cls_type=r[1])
    
    @classmethod
    def fromGeom(cls, geom: Geom_Surface, topods_orientation: int = 2, cls_type: GeomAbs_SurfaceType = None):
        if cls_type is None:
            cls_type = GeomAbs_SurfaceType(GeomAdaptor_Surface(geom).GetType())

        if cls_type in cls.OCC_SURFACE_CLASSES:
            return cls.OCC_SURFACE_CLASSES[cls_type](geom, topods_orientation=topods_orientation)
        else:
            return None
    
    @classmethod
    def fromDict(cls, feature: dict):
        cls_type = feature['type']

        if cls_type in cls.FEATURES_SURFACE_CLASSES:
            return cls.FEATURES_SURFACE_CLASSES[cls_type].fromDict(feature)
        else:
            return None