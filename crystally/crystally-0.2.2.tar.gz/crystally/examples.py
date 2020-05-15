from crystally.core.lattice import Lattice
from crystally.core.lattice import Atom


def ceria():
    """crystal structure of CeO2"""
    return Lattice(
        [[5.499468761674159, 0, 0],
         [0, 5.499468761674159, 0],
         [0, 0, 5.499468761674159]],
        [Atom("Ce", [0, 0, 0], "Ce"),
         Atom("Ce", [0, 0.5, 0.5], "Ce"),
         Atom("Ce", [0.5, 0, 0.5], "Ce"),
         Atom("Ce", [0.5, 0.5, 0], "Ce"),
         Atom("O", [0.25, 0.25, 0.25], "O"),
         Atom("O", [0.75, 0.25, 0.25], "O"),
         Atom("O", [0.25, 0.75, 0.25], "O"),
         Atom("O", [0.25, 0.25, 0.75], "O"),
         Atom("O", [0.75, 0.75, 0.25], "O"),
         Atom("O", [0.25, 0.75, 0.75], "O"),
         Atom("O", [0.75, 0.25, 0.75], "O"),
         Atom("O", [0.75, 0.75, 0.75], "O")])

