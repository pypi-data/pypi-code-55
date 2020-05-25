import numpy as np
from itertools import product


def write_fcs_gpumd(fname_fc, fname_clusters, fcs, order, tol=1e-10):
    """
    Writes force constants of given order in GPUMD format.

    Parameters
    ----------
    fname_fc : str
        name of file which contains the lookup force constants
    fname_clusters : str
        name of file which contains the clusters and the fc lookup index
    fcs : ForceConstants
        force constants
    order : int
        force constants for this order will be written to file
    tol : float
        if the norm of a force constant is less than tol then it is not written.
        if two force-constants are within tol; they are considered equal.
    """
    cluster_lookup, fc_lookup = _get_lookup_data_smart(fcs, order, tol)
    _write_clusters(fname_clusters, cluster_lookup, order)
    _write_fc_lookup(fname_fc, fc_lookup, order)


def _write_fc_lookup(fname, fc_lookup, order):
    """ Writes the lookup force constants to file """
    fmt = '{}' + ' {}'*order
    with open(fname, 'w') as f:
        f.write(str(len(fc_lookup)) + '\n\n')
        for fc in fc_lookup:
            for xyz in product(range(3), repeat=order):
                f.write(fmt.format(*xyz, fc[xyz])+'\n')
            f.write('\n')


def _write_clusters(fname, cluster_lookup, order):
    """ Writes the cluster lookup to file """
    fmt = '{}' + ' {}'*order
    with open(fname, 'w') as f:
        f.write(str(len(cluster_lookup)) + '\n\n')
        for c, i in cluster_lookup.items():
            line = fmt.format(*c, i) + '\n'
            f.write(line)


def _get_lookup_data_smart(fcs, order, tol):
    """ Groups force constants for a given order into groups for which the
    force constant is identical. """
    fc_lookup = []
    cluster_lookup = dict()
    axis = tuple(range(1, order+1))

    clusters = [c for c in fcs._fc_dict.keys() if len(c) == order and np.linalg.norm(fcs[c]) > tol]
    fc_all = np.array([fcs[c] for c in clusters])

    indices = list(range(len(clusters)))
    while len(indices) > 0:
        i = indices[0]
        delta = fc_all[indices] - fc_all[i]
        delta_norm = np.sqrt(np.sum(delta**2, axis=axis))

        inds_to_del = [indices[x] for x in np.where(delta_norm < tol)[0]]
        assert i in inds_to_del

        fc_lookup.append(fc_all[i])
        for j in inds_to_del:
            indices.remove(j)
            cluster_lookup[clusters[j]] = len(fc_lookup)-1
    return cluster_lookup, fc_lookup


def _get_lookup_data_naive(fcs, order, tol):
    """ Groups force constants for a given order into groups for which the
    force constant is identical. """
    fc_lookup = []
    cluster_lookup = dict()
    clusters = [c for c in fcs._fc_dict.keys() if len(c) == order]
    for c in clusters:
        fc1 = fcs[c]
        if np.linalg.norm(fc1) < tol:
            continue
        for i, fc2 in enumerate(fc_lookup):
            if np.linalg.norm(fc1 - fc2) < tol:
                cluster_lookup[c] = i
                break
        else:
            cluster_lookup[c] = len(fc_lookup)
            fc_lookup.append(fc1)
    return cluster_lookup, fc_lookup


def write_fcp_txt(fname, path, n_types, max_order):
    """ Write driver potential file for GPUMD.

    Parameters
    ----------
    fname : str
        file name
    path : str
        path to directory with force constant file
    n_types : int
        number of atom types
    max_order : int
        maximum order of the force constant potential

    Format
    ------
    Format is a simple file containing the following

    fcp number_of_atom_types
    highest_order
    path_to_force_constant_files

    which in practice for a binary system with a sixth order model would mean

    fcp 2
    6
    /path/to/your/folder
    """

    with open(fname, 'w') as f:
        f.write('fcp {}\n'.format(n_types))
        f.write('{}\n'.format(max_order))
        f.write('{}'.format(path.rstrip('/')))  # without a trailing '/'


def write_r0(fname, atoms):
    """
    Write GPUMD r0 file, with reference atomic positions.

    Parameters
    ----------
    fname : str
        name of file to which to write the atomic positions
    atoms : ase.Atoms
        input structure

    """
    line = '{} {} {}\n'
    with open(fname, 'w') as f:
        for a in atoms:
            f.write(line.format(*a.position))
