import unittest
import tfields
from tempfile import NamedTemporaryFile

class IO_Test(unittest.TestCase):
    def test_npz(self):
        p = tfields.Points3D([[1., 2., 3.], [4., 5., 6.], [1, 2, -6]],
                             name='my_points')
        scalars = tfields.Tensors([0, 1, 2], name=42)
        vectors = tfields.Tensors([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
        maps = [tfields.TensorFields([[0, 1, 2], [0, 1, 2]], [42, 21]),
                tfields.TensorFields([[1], [2]], [-42, -21])]
        m = tfields.TensorMaps(vectors, scalars,
                               maps=maps)

        out_file = NamedTemporaryFile(suffix='.npz')
        # Simply give the file name to save
        p.save(out_file.name)
        _ = out_file.seek(0)  # this is only necessary in the test
        p1 = tfields.Points3D.load(out_file.name)
        self.assertTrue(p.equal(p1))
        self.assertEqual(p.coord_sys, p1.coord_sys)

        # The fully nested structure of a TensorMaps object is reconstructed
        out_file_maps = NamedTemporaryFile(suffix='.npz')
        m.save(out_file_maps.name)
        _ = out_file_maps.seek(0)
        m1 = tfields.TensorMaps.load(out_file_maps.name,
                                     allow_pickle=True)
        self.assertTrue(m.equal(m1))
        self.assertEqual(m.maps[3].dtype, m1.maps[3].dtype)

        # Names are preserved
        self.assertEqual(p.name, 'my_points')
        self.assertEqual(m.names, [42])


if __name__ == '__main__':
    unittest.main()
