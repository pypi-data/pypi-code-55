from crystally.core.vectors import *
import copy
import crystally.core.constants as constants
from typing import Union


class Atom:
    """An entry within a :class:`Lattice`.

    The Atom has three propertiers. An element from the periodic table, fractional coordinates in form of a
    :class:`~crystally.core.vectors.FractionalVector` and a sublattice name.

    :param element: string of element name
    :param position: fractional position of the atom
    :param sublattice: name of the sublattice the atom is in
    :return: Atom object
    """

    def __init__(self, element: str ="", position=(0, 0, 0), sublattice: str=""):
        self.element = str(element)
        self._position = FractionalVector(position)
        self.sublattice = str(sublattice)

    def __str__(self):
        string_representation = "Atom:"
        string_representation += f" {self.element:4s} "
        string_representation += f" [{', '.join([f'{coord:13.10f}' for coord in self.position.value])}] "
        string_representation += f" {self.sublattice:8s}"
        return string_representation

    def __repr__(self):
        rep = "Atom("
        rep += repr(self.element)    + ","
        rep += repr(self.position)   + ","
        rep += repr(self.sublattice) + ")"
        return rep

    def __eq__(self, other):
        return self.element == other.element        \
           and self.position == other.position      \
           and self.sublattice == other.sublattice

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = FractionalVector(new_position)


class Lattice:
    """A crystal lattice with atoms and crystal vectors

    :param atoms: string of element name
    :param vectors: fractional position of the atom
    :return: Lattice object
    """

    def __init__(self, vectors=np.identity(3), atoms=None):
        self._vectors = None
        self.atoms = list(atoms) if atoms is not None else None
        self.vectors = vectors

    def __iter__(self):
        return iter(self.atoms)

    def __str__(self):
        string_rep = "Lattice:\n" \
                     + " "*5 + "Vectors:\n"
        for vec in self.vectors:
            components = ["{:13.10f}".format(i) for i in vec]
            string_rep += "{:>23s} {} {}\n".format(*tuple(components))
        string_rep += " "*5 + "Positions:\n"
        for i in range(0, len(self.atoms)):
            string_rep += " "*10
            string_rep += "{: <5d}".format(i)
            string_rep += str(self.atoms[i])
            string_rep += "\n"
        return string_rep

    def __repr__(self):
        rep = "Lattice("
        rep += repr(self.vectors.tolist())  + ","
        rep += repr(self.atoms)             + ")"
        return rep

    def __getitem__(self, item):
        return self.atoms[item]

    def __setitem__(self, key, value):
        self.atoms[key] = value

    def __delitem__(self, key):
        del(self.atoms[key])

    @property
    def vectors(self):
        return self._vectors

    @vectors.setter
    def vectors(self, vec):
        self._vectors = np.array(vec)

    @property
    def size(self):
        """ Calculates the volume of the lattice.

        :return: volume of lattice
        """
        if self.vectors.ndim == 1:
            return np.linalg.norm(self.vectors)
        elif self.vectors.ndim == 2:
            if len(self.vectors) == 1:
                return np.linalg.norm(self.vectors[0])
            elif len(self.vectors) == 2:
                return self.vectors[0].dot(self.vectors[1])
            elif len(self.vectors) == 3:
                return np.cross(self.vectors[0], self.vectors[1]).dot(self.vectors[2])
        else:
            raise NotImplemented("Size property is not compatible with lattice vectors!")

    def sort(self, key=None, tolerance=None):
        """ Sort the lattice with a given key.

        :param key: sorting argument which is used to sort the lattice. The following aruments can be used:

                    1. "element" - will sort according to the atoms element names
                    2. "position" - will sort according to the atoms absolute distance to the lattice origin
                    3. "sublattice" - will sort according to the atoms sublattice name
                    4. :class:`Lattice` - this will sort this lattice according to a different lattice. Equal atoms in
                       this and the other lattice should then have the same position in the atoms lists. Element and
                       Sublattice of the atoms are compared for equality. The position is compared with a tolerance in
                       angstrom. This means that if the atoms are closer together than the tolerance, their position
                       is treated as equal.

        :param tolerance: tolerance parameter which will be used when sorting this lattice with another lattice. If
                          None is specified the default value of constants.ABS_VEC_COMP_TOL is used.
        :return: nothing
        """
        if key is None:
            self.atoms.sort(key=lambda atom: (atom.element, atom.sublattice, atom.position))
        elif key == "element":
            self.atoms.sort(key=lambda atom: atom.element)
        elif key == "position":
            self.atoms.sort(key=lambda atom: self.distance(atom, [0.0, 0.0, 0.0]))
        elif key == "sublattice":
            self.atoms.sort(key=lambda atom: atom.sublattice)
        elif isinstance(key, Lattice):
            self._sort_with_other_lattice(key, tolerance)
        else:
            self.atoms.sort(key=key)
        return None

    def find(self, element=None, sublattice=None, position=None, tolerance=None, first=False):
        """ Search the atom list according to the specified parameters.

        :param element: element name of the atoms to get
        :param sublattice: sublattice name of the atoms to get
        :param position: position of the atoms to get within a tolerance (can be specified)
        :param tolerance: tolerance of positional search in angstrom.
        :param first: If set to `True` the first found atom is returned.
        :return: list of :class:`Atoms <.Atom>` or :class:`Atoms <.Atom>` if first=True or `None` if no atoms satisfy
                 the criteria.
        """
        def element_cond(atom):
            return True if element is None else atom.element == element

        def sublattice_cond(atom):
            return True if sublattice is None else atom.sublattice == sublattice

        def position_cond(atom, tol=tolerance):
            tol = constants.ABS_VEC_COMP_TOL if not tol else tol
            return True if position is None else self.distance(atom, position) < tol

        found_atoms = (atom for atom in self.atoms
                       if element_cond(atom)
                       and sublattice_cond(atom)
                       and position_cond(atom))

        if first is True:
            try:
                return next(found_atoms)
            except StopIteration:
                return None
        else:
            return list(found_atoms)

    def remove(self, atom: Atom):
        """ Removes an atom from the atom list.

        :param atom: :class:`Atoms <.Atom>` that should be removed. This atom has to come from the atom list in the
                     first place.
        :return: None
        """
        for i, a in enumerate(self):
            if id(a) == id(atom):
                del(self[i])
                break
        else:
            raise ValueError("The specified atom is not in the atom list of this lattice.")

    def to_cartesian(self, position):
        """ Translates fractional coordinates to cartesian coordinates.

        :param position: fractional coordinates
        :return: cartesian coordinates
        """
        position = getattr(position, "position", position)
        return self.vectors.dot(np.array(position))

    def to_fractional(self, position, periodic=True):
        """ Translates cartesian coordinates to fractional coordinates.

        :param position: cartesian coordinates
        :param periodic: if periodic is set to `True`. The fractional coordinates are translated
                         to a value between 0 and 1.
        :return: fractional coordinates
        """
        frac_position = np.linalg.inv(self.vectors) @ position
        if periodic:
            return FractionalVector(frac_position).value
        else:
            return frac_position

    def get_in_radius(self, center: Union[np.array, list, Atom], max_radius, min_radius=0.0):
        """ Get all :class:`.Atom` that are in range to a provided position.

        :param center: Search center in fractional coordinates. This can either be a list of coordinates or a :class:`.Atom`.
        :param max_radius: maximal radius in angstrom, that is searched
        :param min_radius: minimal radius in angstrom, that is searched. Default is 0 angstrom.

        :return: List of :class:`.Atom`
        """

        def condition(atom):
            return min_radius <= self.distance(atom, center) <= max_radius
        atom_list = [atom for atom in self.atoms if condition(atom)]
        atom_list.sort(key=lambda atom: self.distance(atom, center))
        return atom_list

    def index(self, position, tolerance=1e-3):
        """ Get the index within the atom list of the :class:`.Atom` at the provided position

        :param position: Position or Atom whose index is searched for
        :param tolerance: Tolerance in angstrom
        :return: index of :class:`.Atom`
        """
        position = getattr(position, "position", position)
        position = np.array(getattr(position, "value", position))
        for i in range(0, len(self.atoms)):
            if self.distance(self.atoms[i].position, position) < tolerance:
                return i
        return None

    def get_element_names(self):
        """ Get all occuring :attr:`Atom.element` names

        :return: List of strings
        """
        element_names = set()
        [element_names.add(x.element) for x in self.atoms]
        return list(element_names)

    def get_sublattice_names(self):
        """ Get all occuring :attr:`Atom.sublattice` names

        :return: List of strings
        """
        sublattice_names = set()
        [sublattice_names.add(x.sublattice) for x in self.atoms]
        return list(sublattice_names)

    def distance(self, position1, position2, periodic=True):
        """ Get the distance between two points

        :param position1: fractional coordinate as list or atom
        :param position2: fractional coordinate as list or atom
        :param periodic: bool, flag that indicates if the distance should be calculated under consideration of
                                periodic boundaries
        :return: float, distance in Angstrom
        """

        position1 = getattr(position1, "position", position1)
        position2 = getattr(position2, "position", position2)

        if periodic:
            position1 = FractionalVector(position1)
            position2 = FractionalVector(position2)
            diff_vector = position2.diff(position1)
        else:
            position1 = np.array(getattr(position1, "value", position1))
            position2 = np.array(getattr(position2, "value", position2))
            diff_vector = position2 - position1

        diff_vector_cartesian = diff_vector.dot(self.vectors)
        return np.sqrt(diff_vector_cartesian.dot(diff_vector_cartesian))

    def increase_distance_rel(self, center, position, rel_increase):
        """ Function to easily manipulate lattices. A center and second position need to be provided. The second
        position is then shifted away from the center position by a provided percentage. The new position is then returned.
        Mind that no variables are changed by this function.

        :param center: fractional coordinates of the center position. Can be a list of coordinates or a :class:`.Atom`.
        :param position: fractional coordinates of the second position. Can be a list of coordinates or a :class:`.Atom`.
        :param rel_increase: distance increase in percent
        :return: new position as :class:`~crystally.core.vectors.FractionalVector`
        """
        # First check if atoms were passed to the function
        center = getattr(center, "position", center)
        position = getattr(position, "position", position)

        # Now convert the vectors to ensure periodicity
        center = FractionalVector(center)
        position = FractionalVector(position)

        # calculate the distance in fractional coordinates from center to position
        diff_vector = center.diff(position)

        # convert everything to cartesian coordinates
        center = self.vectors.dot(center.value)
        diff_vector = self.vectors.dot(diff_vector)

        # calculate the new position in cartesian coordinates
        new_position = center + diff_vector * (1+rel_increase)

        # convert the new position to fractional coordinates
        return FractionalVector(np.linalg.inv(self.vectors).dot(new_position))

    def increase_distance_abs(self, center, position, abs_increase):
        """ Function to easily manipulate lattices. A center and second position need to be provided. The second
        position is then shifted away from the center position by a provided value. The new position is then returned.
        Mind that no variables are changed by this function.

        :param center: fractional coordinates of the center position. Can be a list of coordinates or a :class:`.Atom`.
        :param position: fractional coordinates of the second position. Can be a list of coordinates or a :class:`.Atom`.
        :param abs_increase: Shift in angstrom
        :return: new position as :class:`~crystally.core.vectors.FractionalVector`
        """
        distance = self.distance(center, position)
        rel_distance = abs_increase/distance
        return self.increase_distance_rel(center, position, rel_distance)

    def diff(self, other, tolerance=None):
        """ Find the atomic differences bewteen this and another lattice. Atoms are compared according to element
            sublattice and position. Mind that the fractional position of this and the other lattice are converted
            to cartesian coordinates with the vectors of this lattice.

        :param other: other :class:`.Lattice`.
        :param tolerance: tolerance in angstrom with which the atoms position are compared.
        :return: tuple with two lists, the first list consists of the atoms that were in this lattice, but were not
                 found in the other lattice. The second list contains the atoms that were in the other lattice, but not
                 found in this lattice.
        """

        if not tolerance:
            tolerance = const.ABS_VEC_COMP_TOL

        self_not_found = []
        other_not_found = list(other.atoms)

        for atom1 in self:
            for atom2_id, atom2 in enumerate(other_not_found):
                if self._compare_atoms(atom1, atom2, tolerance):
                        del(other_not_found[atom2_id])
                        break
            else:
                self_not_found.append(atom1)

        return self_not_found, other_not_found

    def _sort_with_other_lattice(self, other, tolerance=None):
        if not tolerance:
            tolerance = const.ABS_VEC_COMP_TOL

        old_order = list(self.atoms)
        new_order = []
        for atom1 in other:
            for atom2_id, atom2 in enumerate(old_order):
                if self._compare_atoms(atom1, atom2, tolerance):
                    new_order.append(atom2)
                    del(old_order[atom2_id])
        new_order += old_order
        self.atoms = new_order

    def _compare_atoms(self, atom1, atom2, dist_tolerance):
        if atom1.element != atom2.element:
            return False
        if atom1.sublattice != atom2.sublattice:
            return False
        if self.distance(atom1, atom2) > dist_tolerance:
            return False
        return True

    @staticmethod
    def from_lattice(lattice, size_x: int = 1, size_y: int = 1, size_z: int = 1):
        """ Create a new lattice with an already existing one. You can also provide size values to expand the lattice.

        :param lattice: the :class:`.Lattice` on which the new lattice is based on
        :param size_x: int, multiplier by which the base lattice is expanded in x direction
        :param size_y: int, see size_x
        :param size_z: int, see size_x
        :return: new :class:`.Lattice`
        """

        new_lattice_size = np.array([size_x, size_y, size_z])
        new_lattice_positions = []

        def reorientate_position(pos, x, y, z): return FractionalVector((pos + np.array([x, y, z])) / new_lattice_size)

        lattice_expansion = ((x, y, z) for x in range(size_x) for y in range(size_y) for z in range(size_z))
        new_lattice_positions += [Atom(element=atom.element,
                                       sublattice=atom.sublattice,
                                       position=reorientate_position(atom.position.value, *coord))
                                  for coord in lattice_expansion for atom in lattice.atoms]

        lattice_vectors = lattice.vectors * new_lattice_size
        new_lattice = Lattice(lattice_vectors, new_lattice_positions)
        new_lattice.sort("element")
        return new_lattice

    @staticmethod
    def grid_atoms(lattice, grid_step):

        def to_grid(lattice, position, round_func):
            position = lattice.vectors @ position
            return tuple(int(x) for x in round_func(np.round(position / grid_step, 10)))

        grid_size = to_grid(lattice, np.array([1, 1, 1]), np.ceil)

        grid = [[[[] for _ in range(grid_size[2])]
                     for _ in range(grid_size[1])]
                     for _ in range(grid_size[0])]

        for atom in lattice:
            x, y, z = to_grid(lattice, atom.position, np.floor)
            grid[x][y][z].append(atom)
        return grid


def concat_lattices(lattice1: Lattice, lattice2: Lattice, direction: int):
    for i in range(lattice1.vectors.shape[0]):
        if i == direction:
            continue
        if not np.allclose(lattice1.vectors[i], lattice2.vectors[i], atol=1e-10):
            raise ValueError("shape of lattices does not match: "
                             "lattice1: {} lattice2: {}".format(str(lattice1.vectors[i]), lattice2.vectors[i]))
    new_lattice = Lattice(vectors=lattice1.vectors, atoms=[])
    new_lattice.vectors[direction] = lattice1.vectors[direction] + lattice2.vectors[direction]
    for atom in lattice1.atoms:
        new_atom = copy.copy(atom)
        new_atom.position = FractionalVector(atom.position.value.dot(lattice1.vectors).dot(np.linalg.inv(new_lattice.vectors)))
        new_lattice.atoms.append(new_atom)

    for atom in lattice2.atoms:
        new_atom = copy.copy(atom)
        shift = new_atom.position.value * 0
        shift[direction] = 1
        shift_cart = shift.dot(lattice1.vectors)
        new_position = new_atom.position.value.dot(lattice2.vectors) + shift_cart
        new_position = new_position.dot(np.linalg.inv(new_lattice.vectors))
        new_atom.position = FractionalVector(new_position)
        new_lattice.atoms.append(new_atom)

    return new_lattice
