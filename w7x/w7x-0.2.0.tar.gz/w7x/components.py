import logging
import tfields
import numpy as np

import w7x
from w7x import core


class Points3D(core.BasePoints3D):
    ws_server = w7x.Server.addr_components_db


class Base(core.Base):
    """
    Field Line Server Base
    """
    ws_server = w7x.Server.addr_components_db


class Polygon(Base):
    """
        element.vertices gives you the three points numbers to a triangle.
        This is normally refered to as face
    """

    prop_defaults = {
        'vertices': None
    }


class MeshedModel(Base):
    """
    Args:
        multiple ways:
            vertices (list)
            faces (list)

            - or -

            group from ObjFile

            - or -

            tfields.Mesh3D object
    Attributes:
        nodes (Points3D): = vertices (coordinates) of the points.
        elements (list[Polygon]): = faces (always three indices of points for a
            triangle). Starting at 1 here
    Examples:
        use with Mesh3D as inp
        >>> from w7x.flt import MeshedModel
        >>> import tfields
        >>> m = tfields.Mesh3D([[1,2,3], [3,3,3], [0,0,0], [5,6,7]],
        ...                    faces=[[0, 1, 2], [1, 2, 3]])
        >>> mm = MeshedModel(m)

        Get the osa type, in this case for field line server
        >>> fls = mm.as_input()

        return Mesh3D works
        >>> bool((m == mm.as_mesh3d()).all())
        True

        create with meshed Model from fls works
        >>> m2 = MeshedModel(fls).as_mesh3d()
        >>> assert tfields.Points3D(m2).equal(
        ...     [[ 1.,  2.,  3.],
        ...      [ 3.,  3.,  3.],
        ...      [ 0.,  0.,  0.],
        ...      [ 5.,  6.,  7.]])
        >>> assert tfields.Tensors(m2.faces).equal([[0, 1, 2], [1, 2, 3]])

    """

    prop_defaults = {
        'nodes': None,
        'elements': None,
        'nodesIds': None,
        'elementsIds': None
    }

    def __init__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 1:
            logging.error(" Implementation did not work.")
            raise NotImplementedError(
                " Implementation with args %s not yet implemented!" % args)
        elif len(args) == 1 and issubclass(args[0].__class__, tfields.Mesh3D):
            mesh3D = args.pop(0)
            nodes = Points3D(mesh3D)
            faces = mesh3D.faces + 1
            kwargs['nodes'] = kwargs.pop('nodes', nodes)
            kwargs['elements'] = kwargs.pop(
                'elements',
                [Polygon(vertices=face) for face in faces])
        super(MeshedModel, self).__init__(*args, **kwargs)

    @classmethod
    def from_mm_id(cls, mm_id):
        compDBServer = w7x.get_server(w7x.Server.addr_components_db)
        meshedModelFLSType = compDBServer.service.getComponentData(mm_id)[0]
        return cls(meshedModelFLSType)

    def as_mesh3d(self):
        faces = np.array([pol.vertices for pol in self.elements])
        faces -= 1
        return tfields.Mesh3D(Points3D(self.nodes), faces=faces)


class HistoryNote(Base):
    prop_defaults = {
        'comment': None,  # str
        'author': None,  # str
        'date': None,  # datetime
        'method': None,  # str
    }


class ComponentStorageInfo(Base):
    prop_defaults = {
        'comment': None,  # str
        'polygonTypes': None,  # List[int]
        'numNodes': None,  # int
        'id': None,  # str
        'machine': 'w7x',  # str, ws default is None
        'min': None,  # List[float]
        'numElements': None,  # int
        'state': None,  # str
        'location': None,  # str
        'accuracy': None,  # float
        'max': None,  # List[float]
        'name': None,  # str
        'subids': None,  # List[str]
        'author': None,  # str
        'method': None,  # str
        'resolution': None,  # float
        'hisotry': None,  # List(HistoryNote)
    }


class FullComponentEntry(Base):
    prop_defaults = {'info': None,  # ComponentStorageInfo
                     'data': None,  # MeshedModel
                     }

    @property
    def parent(self):
        return self._parent


# csi = ComponentStorageInfo()
# fci = FullComponentEntry(info=csi)
# # csi.history = [{"timeStamp":"1311918723","author":"boz","method":"jk2Ansys","comment":"created"}]
# print(fci.as_input())
