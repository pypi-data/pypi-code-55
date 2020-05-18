import unittest
import tfields


class Base_Check(object):
    def test_merging(self):
        merged_without_templates = type(self._instances[0])\
            .merged(*self._instances)
        merged, templates = type(self._instances[0])\
            .merged(*self._instances, return_templates=True)
        self.assertTrue(merged_without_templates.equal(merged))
        self.assertTrue(len(templates), len(self._instances))
        for template, inst in zip(templates, self._instances):
            self.assertEqual(template.dim, 0)  # merging templates save meory
            cut = merged.cut(template)
            self.demand_equal_cut(inst, template, cut)

    def demand_equal_cut(self, inst, template, cut):
        pass


class Tensors_Empty_Test(Base_Check, unittest.TestCase):
    def setUp(self):
        self._instances = [tfields.Tensors([], dim=3) for i in range(3)]


class TensorFields_Empty_Test(Base_Check, unittest.TestCase):
    def setUp(self):
        self._fields = []
        self._instances = [tfields.TensorFields([], dim=3) for i in range(3)]


class TensorMaps_Empty_Test(Base_Check, unittest.TestCase):
    def setUp(self):
        self._instances = [tfields.TensorMaps([], dim=3) for i in range(3)]

    def demand_equal_cut(self, inst, template, cut):
        self.assertEqual(len(inst.maps), len(cut.maps))
        self.assertEqual(len(cut.maps), len(template.maps))
        for mp_dim, mp in inst.maps.items():
            cut_map = cut.maps[mp_dim]
            self.assertEqual(len(mp),
                             len(cut_map))
            self.assertEqual(tfields.dim(mp),
                             tfields.dim(cut_map))
        self.assertTrue(inst.equal(cut))  # most important


class TensorFields_Test(TensorFields_Empty_Test):
    def setUp(self):
        base = [(-5, 5, 7)] * 3
        self._fields = [tfields.Tensors.grid(*base, coord_sys='cylinder'),
                        tfields.Tensors(range(7**3))]
        tensors = tfields.Tensors.grid(*base)
        self._instances = [tfields.TensorFields(tensors, *self._fields)
                           for i in range(3)]


class TensorMaps_Test(TensorMaps_Empty_Test):
    def setUp(self):
        base = [(-1, 1, 2)] * 2
        tensors = tfields.Tensors.grid(*base, (-1,1,1))
        self._fields = [tfields.Tensors.grid(*base, coord_sys='cylinder'),
                        tfields.Tensors(range(len(tensors)))]
        self._maps_tensors = [
            [[0, 2],
             [1, 3]],
            [[0, 1, 3],
             [1, 2, 3],
             [1, 2, 0]],
            [[2]],
        ]
        self._maps_fields = [
            [[3, 25]],
            [[42., 21., 11]],
            [[111]],
        ]
        self._maps = [tfields.TensorFields(map_tensors,
                                           *map_fields) for map_tensors,
                      map_fields in zip(self._maps_tensors, self._maps_fields)]
        self._instances = [tfields.TensorMaps(tensors, *self._fields,
                                              maps=self._maps)
                           for i in range(2)]


class Mesh3D_Test(TensorMaps_Empty_Test):
    def setUp(self):
        base = [(-1, 1, 2)] * 2
        tensors = tfields.Tensors.grid(*base, (-1,1,1))
        self._fields = [tfields.Tensors.grid(*base, coord_sys='cylinder'),
                        tfields.Tensors(range(len(tensors)))]
        self._maps_tensors = [
            [[0, 1, 3],
             [1, 2, 3],
             [1, 2, 0]],
        ]
        self._maps_fields = [
            [[42., 21., 11]],
        ]
        self._maps = [tfields.TensorFields(map_tensors,
                                           *map_fields) for map_tensors,
                      map_fields in zip(self._maps_tensors, self._maps_fields)]
        self._instances = [tfields.TensorMaps(tensors, *self._fields,
                                              maps=self._maps)
                           for i in range(2)]


if __name__ == '__main__':
    a = TensorMaps_Empty_Test()
    unittest.main()
