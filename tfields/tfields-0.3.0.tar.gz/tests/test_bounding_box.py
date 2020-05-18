import unittest
import tfields
import numpy as np

class BoundingBox_Test(unittest.TestCase):
    def setUp(self):
        self._mesh = tfields.Mesh3D.grid((5.6, 6.2, 3),
                                         (-0.25, 0.25, 4),
                                         (-1, 1, 10))

        self._cuts = {'x': [5.7, 6.1],
                      'y': [-0.2, 0, 0.2],
                      'z': [-0.5, 0.5]}

    def test_tree(self):
        # test already in doctests.
        tree = tfields.bounding_box.Node(self._mesh,
                                         self._cuts,
                                         at_intersection='keep')
        leaves = tree.leaves()
        leaves = tfields.bounding_box.Node.sort_leaves(leaves)
        meshes = [leaf.mesh for leaf in leaves]
        templates = [leaf.template for leaf in leaves]
        special_leaf = tree.find_leaf([5.65, -0.21, 0])


class Searcher_Test(unittest.TestCase):
    def setUp(self):
        self._mesh = tfields.Mesh3D.grid((0, 1, 2), (1, 2, 2), (2, 3, 2))

    def test_tree(self):
        tree = tfields.bounding_box.Searcher(self._mesh, n_sections=[5, 5, 5])
        points = tfields.Tensors([[0.5, 1, 2.1],
                                  [0.5, 0, 0],
                                  [0.5, 2, 2.1],
                                  [0.5, 1.5, 2.5]])
        box_res = tree.in_faces(points, delta=0.0001)
        usual_res = self._mesh.in_faces(points, delta=0.0001)
        self.assertTrue(np.array_equal(box_res, usual_res))


if __name__ == '__main__':
    unittest.main()
