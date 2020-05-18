import numpy as np
from tempfile import NamedTemporaryFile
import pickle
import pathlib
import unittest
import tfields

ATOL = 1e-8


class Base_Check(object):
    def demand_equal(self, other):
        self.assertIsInstance(other, type(self._inst))

    def demand_deep_copy(self, other):
        self.demand_equal(other)
        self.assertIsNot(self._inst, other)

    def test_pickle(self):
        with NamedTemporaryFile(suffix='.pickle') as out_file:
            pickle.dump(self._inst,
                        out_file)
            out_file.flush()
            out_file.seek(0)
            reloaded = pickle.load(out_file)

        self.demand_equal(reloaded)

    def test_deep_copy(self):
        from copy import deepcopy
        other = deepcopy(self._inst)
        self.demand_deep_copy(other)

    def test_implicit_copy(self):
        other = type(self._inst)(self._inst)
        self.demand_deep_copy(other)

    def test_explicit_copy(self):
        other = self._inst.copy()
        self.demand_deep_copy(other)

    def test_save_npz(self):
        out_file = NamedTemporaryFile(suffix='.npz')
        self._inst.save(out_file.name)
        _ = out_file.seek(0)  # this is only necessary in the test
        load_inst = type(self._inst).load(out_file.name)
        # allow_pickle=True)  ?

        self.demand_equal(load_inst)

    def test_dict(self):
        d = self._inst._as_dict()
        other = type(self._inst)._from_dict(d)
        self.demand_equal(other)

    def tearDown(self):
        del self._inst


class AbstractNdarray_Check(Base_Check):
    pass


class Tensors_Check(AbstractNdarray_Check):
    """
    Testing derivatives of Tensors
    """
    _inst = None

    def demand_equal(self, other, atol=False, transformed=False):
        super().demand_equal(other)
        if atol:
            self.assertTrue(self._inst.equal(other, atol=ATOL))
        else:
            self.assertTrue(self._inst.equal(other))
        if not transformed:
            self.assertEqual(self._inst.coord_sys, other.coord_sys)
        self.assertEqual(self._inst.name, other.name)

    def test_slice_indexing(self):
        self.demand_index_equal(slice(0, None, None), 'type')

    def test_pick_indexing(self):
        self.demand_index_equal(0, (np.ndarray, np.integer, np.float))

    def test_mask_indexing(self):
        mask = np.array([True if i % 2 == 0 else False
                         for i in range(len(self._inst))])
        self.demand_index_equal(mask, 'type')

    def test_iteration(self):
        # iteration
        iterator = iter(self._inst)
        if len(self._inst) > 0:
            next(iterator)

    def demand_index_equal(self, index, check_type):
        if check_type == 'type':
            check_type = type(self._inst)
        tensors = np.array(self._inst)
        if len(self._inst) > 0:

            item = self._inst[index]
            self.assertTrue(np.array_equal(item, tensors[index]))
            self.assertIsInstance(item, check_type)

    def check_indexing(self):
        if not self._inst.fields and len(self._inst) == 0:
            return
        fields = [np.array(field) for field in self._inst.fields]
        for f, field in enumerate(fields):
            self._inst.fields[f]

    def test_self_equality(self):
        # Test equality
        self.demand_equal(self._inst)
        transformer = self._inst.copy()
        transformer.transform(tfields.bases.CYLINDER)
        self.demand_equal(transformer, atol=True, transformed=True)
        # self.assertIs(self._inst, np.asarray(self._inst))  # TODO investigate

    def test_cylinderTrafo(self):
        # Test coordinate transformations in circle
        transformer = self._inst.copy()
        transformer.transform(tfields.bases.CYLINDER)
        if len(self._inst) > 0:
            self.assertFalse(np.array_equal(self._inst, transformer))
        transformer.transform(tfields.bases.CARTESIAN)
        self.demand_equal(transformer, atol=True, transformed=True)

    def test_spericalTrafo(self):
        # Test coordinate transformations in circle
        transformer = self._inst.copy()
        transformer.transform(tfields.bases.SPHERICAL)
        transformer.transform(tfields.bases.CARTESIAN)
        self.demand_equal(transformer, atol=True, transformed=True)

    def test_basic_merge(self):
        # create 3 copies with different coord_sys
        merge_list = [self._inst.copy() for i in range(3)]
        merge_list[0].transform(tfields.bases.CARTESIAN)
        merge_list[1].transform(tfields.bases.CYLINDER)
        merge_list[2].transform(tfields.bases.SPHERICAL)

        # merge them and check that the first coord_sys is taken
        obj = type(self._inst).merged(*merge_list)
        self.assertTrue(obj.coord_sys == tfields.bases.CARTESIAN)

        # check that all copies are the same also with new coord_sys
        for i in range(len(merge_list)):
            value = np.allclose(merge_list[0],
                                obj[i * len(self._inst): (i + 1) *
                                    len(self._inst)],
                                atol=ATOL)
            self.assertTrue(value)

        obj_cs = type(self._inst).merged(*merge_list,
                                         coord_sys=tfields.bases.CYLINDER)
        for i in range(len(merge_list)):
            value = np.allclose(merge_list[1],
                                obj_cs[i * len(self._inst): (i + 1) *
                                       len(self._inst)],
                                atol=ATOL)
            self.assertTrue(value)


class TensorFields_Check(Tensors_Check):
    def test_fields(self):
        self.assertIsNotNone(self._inst.fields)
        if self._inst.fields:
            # field is of type list
            self.assertTrue(isinstance(self._inst.fields, list))
            self.assertTrue(len(self._inst.fields) == len(self._fields))

            for field, target_field in zip(self._inst.fields, self._fields):
                self.assertTrue(np.array_equal(field, target_field))
                # fields are copied not reffered by a pointer
                self.assertFalse(field is target_field)

    def demand_index_equal(self, index, check_type):
        super().demand_index_equal(index, check_type)

        if len(self._inst) > 0:
            item = self._inst[index]
            for i, field in enumerate(self._inst.fields):
                if check_type == 'type':
                    check_type = type(self._inst.fields[i])
                self.assertTrue(np.array_equal(
                    item.fields[i], np.array(self._inst.fields[i])[index]))
                self.assertIsInstance(item.fields[i], check_type)

    def demand_deep_copy(self, other):
        super().demand_deep_copy(other)
        self.assertIsNot(self._inst.fields, other.fields)
        for i in range(len(self._inst.fields)):
            self.assertIsNot(self._inst.fields[i], other.fields[i])


class TensorMaps_Check(TensorFields_Check):
    def test_maps(self):
        self.assertIsNotNone(self._inst.maps)

    def test_cleaned(self):
        clean = self._inst.cleaned()
        # no faces are removed
        for map_dim in self._inst.maps:
            self.assertEqual(len(self._inst.maps[map_dim]),
                             len(clean.maps[map_dim]))

    def demand_index_equal(self, index, check_type):
        super().demand_index_equal(index, check_type)
        # TODO: this is hard to check generically

    def demand_deep_copy(self, other):
        super().demand_deep_copy(other)
        self.assertIsNot(self._inst.maps, other.maps)
        for i in self._inst.maps:
            self.assertIsNot(self._inst.maps[i], other.maps[i])


"""
EMPTY TESTS
"""


class Tensors_Empty_Test(Tensors_Check, unittest.TestCase):
    def setUp(self):
        self._inst = tfields.Tensors([], dim=3)


class TensorFields_Empty_Test(TensorFields_Check, unittest.TestCase):
    def setUp(self):
        self._fields = []
        self._inst = tfields.TensorFields([], dim=3)


class TensorMaps_Empty_Test(TensorMaps_Check, unittest.TestCase):
    def setUp(self):
        self._fields = []
        self._inst = tfields.TensorMaps([], dim=3)
        self._maps = []
        self._maps_fields = []


class TensorFields_Test(Tensors_Check, unittest.TestCase):
    def setUp(self):
        base = [(-5, 5, 11)] * 3
        self._fields = [tfields.Tensors.grid(*base, coord_sys='cylinder'),
                        tfields.Tensors(range(11**3))]
        tensors = tfields.Tensors.grid(*base)
        self._inst = tfields.TensorFields(tensors, *self._fields)

        self.assertTrue(self._fields[0].coord_sys, 'cylinder')
        self.assertTrue(self._fields[1].coord_sys, 'cartesian')


class TensorMaps_Test(Tensors_Check, unittest.TestCase):
    def setUp(self):
        base = [(-1, 1, 3)] * 3
        tensors = tfields.Tensors.grid(*base)
        self._fields = [tfields.Tensors.grid(*base, coord_sys='cylinder'),
                        tfields.Tensors(range(len(tensors)))]
        self._maps_tensors = [[[0, 0, 0],
                               [1, 2, 3],
                               [1, 5, 9]],
                              [[0, 4],
                               [1, 3]],
                              [[42]]]
        self._maps_fields = [[[42., 21., 11]],
                             [[3, 25]],
                             [[111]]]
        self._maps = [tfields.TensorFields(map_tensors,
                                           *map_fields) for map_tensors,
                      map_fields in zip(self._maps_tensors, self._maps_fields)]
        self._inst = tfields.TensorMaps(tensors, *self._fields,
                                        maps=self._maps)

    def test_legacy(self):
        this_dir = pathlib.Path(__file__).parent
        legacy_file = this_dir / 'resources/TensorMaps_0.2.1_ce3ea1fb69058dc39815be65f485abebb487a6bd.npz'  # NOQA
        tm = tfields.TensorMaps.load(legacy_file)
        self.assertTrue(self._inst.equal(tm))


class TensorMaps_Indexing_Test(unittest.TestCase):
    def setUp(self):
        tensors = np.arange(10).reshape((-1, 1))
        self._maps_tensors = [[[0, 0, 0],
                               [1, 2, 3],
                               [3, 5, 9]],
                              [[6, 4],
                               [7, 8]],
                              [[7]]]
        self._inst = tfields.TensorMaps(tensors,
                                        maps=self._maps_tensors)

    def test_pick_indexing(self):
        pick = self._inst[7]
        self.assertTrue(pick.equal([7]))
        self.assertTrue(np.array_equal(pick.maps[1], [[0]]))
        self.assertTrue(len(pick.maps), 1)

        pick = self._inst[0]
        self.assertTrue(pick.equal([[0]]))
        self.assertTrue(np.array_equal(pick.maps[3], [[0, 0, 0]]))
        self.assertTrue(len(pick.maps), 1)

    def test_slice_indexing(self):
        slce = self._inst[1:7]
        self.assertTrue(slce.equal([[1], [2], [3], [4], [5], [6]]))
        self.assertTrue(np.array_equal(slce.maps[3], [[0, 1, 2]]))
        self.assertTrue(np.array_equal(slce.maps[2], [[5, 3]]))
        self.assertTrue(len(slce.maps), 2)

    def test_mask_indexing(self):
        mask = self._inst[np.array([False, True, True, True, True,
                                    True, True, False, False, False])]
        self.assertTrue(mask.equal([[1], [2], [3], [4], [5], [6]]))
        self.assertTrue(np.array_equal(mask.maps[3], [[0, 1, 2]]))
        self.assertTrue(np.array_equal(mask.maps[2], [[5, 3]]))
        self.assertTrue(len(mask.maps), 2)


class TensorMaps_NoFields_Test(Tensors_Check, unittest.TestCase):
    def setUp(self):
        self._inst = tfields.TensorMaps(
            [[1, 2, 3], [3, 3, 3], [0, 0, 0], [5, 6, 7]],
            maps=[[[0, 1, 2], [1, 2, 3]], [[1]], [[0, 1, 2, 3]]]
        )


class Maps_Test(Base_Check, unittest.TestCase):
    def demand_equal(self, other):
        super().demand_equal(other)
        self._inst.equal(other)

    def setUp(self):
        self._inst = tfields.Maps(
            [[[0, 0, 0],
              [1, 2, 3],
              [1, 5, 9]],
             [[0, 4],
              [1, 3]],
             [[42]]])


class Maps_Init_Test(Maps_Test):
    def setUp(self):
        self._inst = tfields.Maps({3: [[0, 1, 2]], 0: [[]]})


class Maps_Rigid_Test(Maps_Test):
    def setUp(self):
        rig = tfields.Maps({0: [[1, 2, 42]], 3: [1]})
        self.assertIsInstance(rig[0], tfields.TensorFields)
        self.assertIsInstance(rig[3], tfields.TensorFields)
        self.assertEqual(tfields.dim(rig[0]), 3)
        self.assertEqual(tfields.dim(rig[3]), 1)
        self.assertEqual(tfields.rank(rig[0]), 1)
        self.assertEqual(tfields.rank(rig[3]), 0)
        self._inst = rig


class Container_Check(AbstractNdarray_Check):
    def demand_equal(self, other):
        super().demand_equal(other)
        for i, item in enumerate(self._inst.items):
            if issubclass(type(item), tfields.core.AbstractNdarray):
                self.assertTrue(other.items[i].equal(item))
            else:
                self.assertEqual(other.items[i], item)
            try:
                self._inst.labels[i]
            except (IndexError, TypeError):
                pass
            else:
                self.assertEqual(other.labels[i], self._inst.labels[i])

    def test_item(self):
        if len(self._inst.items) > 0:
            self.assertEqual(len(self._inst), len(self._inst))
            self.assertEqual(type(self._inst), type(self._inst))


class Container_Test(Container_Check, unittest.TestCase):
    def setUp(self):
        sphere = tfields.Mesh3D.grid(
            (1, 1, 1),
            (-np.pi, np.pi, 3),
            (-np.pi / 2, np.pi / 2, 3),
            coord_sys='spherical')
        sphere2 = sphere.copy() * 3
        self._inst = tfields.Container([sphere, sphere2], labels=['test'])


if __name__ == '__main__':
    unittest.main()
