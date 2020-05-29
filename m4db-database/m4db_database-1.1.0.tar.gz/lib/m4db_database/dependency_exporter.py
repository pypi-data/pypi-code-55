r"""
A set of utility functions that are useful when exporting data.
"""

from m4db_database.sessions import get_session

from m4db_database.orm import Model
from m4db_database.orm import NEB


def model_dependencies(unique_ids):
    r"""
    Returns a list of geometry and model unique ids with resolved dependencies.
    Args:
        unique_ids: an initial list of Model unique ids.

    Returns:
        a pair containing a python set of geometry unique ids and a python set of model unique ids
    """
    geometry_unique_ids = set()


def neb_dependencies(unique_ids, session):
    r"""
    Returns a list of geometry, model and NEB path unique ids with resolved dependencies.
    Args:
        unique_ids: an initial list of NEB path unique ids.
        session: the database session object.

    Returns:
        A three-tuple containing a set of geometry unique ids, a set of model unique ids and a set of NEB unique ids.

    """
    geometry_unique_ids = set()
    model_unique_ids = set()
    neb_unique_ids = set()

    neb_unique_ids_stack = unique_ids[:]

    while len(neb_unique_ids_stack) > 0:
        uid = neb_unique_ids_stack.pop()

        neb = session.query(NEB).filter(NEB.unique_id == uid).one()

        if neb.parent_neb is not None:
            neb_unique_ids_stack.append(neb.parent_neb.unique_id)

        neb_unique_ids.add(neb.unique_id)
        model_unique_ids.add(neb.start_model.unique_id)
        model_unique_ids.add(neb.end_model.unique_id)

        if neb.start_model.geometry.unique_id == neb.end_model.geometry.unique_id:
            geometry_unique_ids.add(neb.start_model.geometry.unique_id)
            geometry_unique_ids.add(neb.end_model.geometry.unique_id)
        else:
            raise ValueError(
                "Start model (uid: {}) and end model (uid: {}) of path (uid: {}) have different geometries!".format(
                    neb.start_model.unique_id,
                    neb.end_model.unique_id,
                    neb.unique_id
                ))

    return list(geometry_unique_ids), list(model_unique_ids), list(neb_unique_ids)
