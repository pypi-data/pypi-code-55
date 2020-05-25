"""
This module introduces the ForceConstantPotential object which acts as the
finalized force constant model.
"""

import pickle
from collections import Counter

import numpy as np
from .force_constant_model import ForceConstantModel
from .core.orbits import Orbit
from .core.orbits import OrientationFamily
from .core.tensors import rotation_to_cart_coord, rotate_tensor


# TODO: Fix the relation with cluster space
class ForceConstantPotential:
    """ A finalized force constant model. Can produce force constants for any
    structure compatible with the structure for which the model was set up.

    Parameters
    ----------
    cs : ClusterSpace
        The cluster space the model is based upon
    parameters : numpy.ndarray
        The fitted paramteres
    metadata : dict
        metadata dictionary, will be pickled when object is written to file
    """

    def __init__(self, cs, parameters, metadata=None):

        self._prim = cs.primitive_structure.copy()
        self.cluster_list = cs.cluster_list.copy()
        self.atom_list = cs.atom_list.copy()
        self.orbits = []
        self.spacegroup = cs.spacegroup
        self._config = cs._config

        # add metadata
        if metadata is None:
            metadata = dict()
        self._metadata = metadata
        self._add_default_metadata()

        # Extract the eigentensors from the cluster space and use the paramters
        # to construct the finalized force constants
        parameters = cs._map_parameters(parameters)
        p = 0
        for orb in cs.orbits:
            new_orbit = Orbit()
            fc = np.zeros(orb.eigentensors[0].shape)
            for et, a in zip(orb.eigentensors, parameters[p:]):
                fc += et * a
            new_orbit.force_constant = fc
            new_orbit.order = orb.order
            new_orbit.radius = orb.radius
            new_orbit.maximum_distance = orb.maximum_distance
            for of in orb.orientation_families:
                new_of = OrientationFamily()
                new_of.cluster_indices = of.cluster_indices.copy()
                sym_ind = of.symmetry_index
                R = rotation_to_cart_coord(cs.rotation_matrices[sym_ind],
                                           self.primitive_structure.cell)
                fc = rotate_tensor(new_orbit.force_constant, R.T)
                perm = cs.permutations[of.permutation_indices[0]]
                new_of.force_constant = fc.transpose(perm)
                new_orbit.orientation_families.append(new_of)
            self.orbits.append(new_orbit)
            p += len(orb.eigentensors)

    @property
    def symprec(self):
        return self._config['symprec']

    @staticmethod
    def read(f):
        """Reads a force constant potential from file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to load from (file object)

        Returns
        -------
        ForceConstantPotential
            the original object as stored in the file
        """
        if isinstance(f, str):
            with open(f, 'rb') as fobj:

                # TODO: Remove this once better read/write functions in place
                # This allows for reading FCPs with ASE-3.17 and 3.18
                from .core.atoms import Atoms
                fcp = pickle.load(fobj)
                _prim = fcp._prim

                # get cell
                if hasattr(_prim, '_cell'):  # 3.17
                    cell = _prim._cell
                else:                       # 3.18
                    cell = _prim.cell[:]

                # assume PBC True (as it has to be True in hiphive)
                pbc = [True, True, True]

                # finalize
                new_prim = Atoms(
                    symbols=_prim.symbols, positions=_prim.positions, cell=cell, pbc=pbc)
                fcp._prim = new_prim
                return fcp
        else:
            try:
                return pickle.load(f)
            except Exception:
                raise Exception('Failed loading from file.')

    def write(self, f):
        """Writes a force constant potential to file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to write to (file object)
        """
        if isinstance(f, str):
            with open(f, 'wb') as fobj:
                pickle.dump(self, fobj)
        else:
            try:
                pickle.dump(self, f)
            except Exception:
                raise Exception('Failed writing to file.')

    @property
    def metadata(self):
        """ dict : metadata associated with force constant potential """
        return self._metadata

    @property
    def primitive_structure(self):
        """ ase.Atoms : atomic structure """
        return self._prim.copy()

    @property
    def orbit_data(self):
        """ List[dict] : list of dictionaries containing detailed information for
                         each orbit, e.g. cluster radius and force constant
        """
        data = []
        for orbit_index, orbit in enumerate(self.orbits):
            d = {}
            d['index'] = orbit_index
            d['order'] = orbit.order
            d['radius'] = orbit.radius
            d['maximum_distance'] = orbit.maximum_distance
            d['n_clusters'] = len(orbit.orientation_families)

            types = []
            for atom_ind in self.cluster_list[orbit.prototype_index]:
                types.append(self.primitive_structure.numbers[
                    self.atom_list[atom_ind].site])
            d['prototype_cluster'] = self.cluster_list[orbit.prototype_index]
            d['prototype_atom_types'] = types

            d['geometrical_order'] = len(set(d['prototype_cluster']))
            d['force_constant'] = orbit.force_constant
            d['force_constant_norm'] = np.linalg.norm(orbit.force_constant)
            data.append(d)
        return data

    def get_force_constants(self, atoms):
        """ Return the force constants of a compatible structure.

        Parameters
        ----------
        atoms : ase.Atoms
            input structure

        Returns
        -------
        ForceConstants
            force constants
        """
        return ForceConstantModel(atoms, self).get_force_constants()

    def __str__(self):
        orbits = self.orbit_data
        orbit_counts = Counter([orbit['order'] for orbit in orbits])
        cluster_counts = Counter()
        for orbit in orbits:
            cluster_counts[orbit['order']] += orbit['n_clusters']

        n = 54
        s = []
        s.append(' ForceConstantPotential '.center(n, '='))
        s.append('Spacegroup {}'.format(self.spacegroup))
        s.append('Cell:\n{}'.format(self.primitive_structure.cell))
        s.append('Basis:\n{}'.format(self.primitive_structure.basis))
        s.append('Numbers: {}'.format(self.primitive_structure.numbers))
        for order in sorted(orbit_counts.keys()):
            s.append('Order {}, #orbits {}, #cluster {}'.format(
                     order, orbit_counts[order], cluster_counts[order]))
        s.append('Total number of orbits: {} '.format(len(orbits)))
        s.append('total number of clusters: {} '
                 .format(sum(cluster_counts.values())))
        s.append(''.center(n, '='))
        return '\n'.join(s)

    def __repr__(self):
        return 'ForceConstantPotential(ClusterSpace({!r}, ...), [...])'.format(
            self.primitive_structure)

    def _add_default_metadata(self):
        """Adds default metadata to metadata dict."""
        import getpass
        import socket
        from datetime import datetime
        from . import __version__ as hiphive_version

        self._metadata['date_created'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self._metadata['username'] = getpass.getuser()
        self._metadata['hostname'] = socket.gethostname()
        self._metadata['hiphive_version'] = hiphive_version
