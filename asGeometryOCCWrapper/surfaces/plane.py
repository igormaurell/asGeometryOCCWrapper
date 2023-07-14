from OCC.Core.Geom import Geom_Plane
from OCC.Core.gp import gp_Pnt, gp_Ax3, gp_Dir

import numpy as np

from .base_surfaces import BaseElementarySurface

class Plane(BaseElementarySurface):

    @staticmethod
    def getType():
        return 'Plane'
    
    @staticmethod
    def getColor():
        return (255, 0, 0)
    
    @staticmethod
    def adaptor2Geom(adaptor):
        return Geom_Plane(adaptor.Plane())
    
    @classmethod
    def _geomFromDict(cls, features: dict):
        geom = Geom_Plane(cls._features2Ax3(features))
        return geom
