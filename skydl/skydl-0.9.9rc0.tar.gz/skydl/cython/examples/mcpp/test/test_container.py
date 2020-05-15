import unittest
import skydl.cython.examples.mcpp.test.container_unit_tests as container_unit_tests


class EmplaceTest(unittest.TestCase):
    def test_emplace_object_move_vector(self):
        x=container_unit_tests.run_emplace_object_move_vector()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_emplace_object_move_map(self):
        x=container_unit_tests.run_emplace_object_move_map()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_emplace_move_vector(self):
        x=container_unit_tests.run_emplace_move_vector()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_emplace_vector_unique_ptr(self):
        x=container_unit_tests.run_emplace_vector_unique_ptr()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_emplace_vector(self):
        x=container_unit_tests.run_emplace_vector()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)

class EmplacePosTest(unittest.TestCase):
    def test_emplace_object_pos_move_vector(self):
        x = container_unit_tests.run_emplace_object_pos_move_vector()
        self.assertEqual(x['size'],2)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_emplace_pos_move_vector_unique_ptr(self):
        x = container_unit_tests.run_emplace_pos_move_vector_unique_ptr()
        self.assertEqual(x['size'],2)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_emplace_pos_move_vector_unique_ptr2(self):
        x = container_unit_tests.run_emplace_pos_move_vector_unique_ptr2()
        self.assertEqual(x['size'],2)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)

class PushBackTest(unittest.TestCase):
    def test_push_back_move_vector(self):
        x=container_unit_tests.run_push_back_move_vector()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)

class PushFrontTest(unittest.TestCase):
    def test_push_front_move_list(self):
        x=container_unit_tests.run_push_front_move_list()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)
    def test_push_front_move_deque(self):
        x=container_unit_tests.run_push_front_move_deque()
        self.assertEqual(x['size'],1)
        self.assertEqual(x['first'],2)
        self.assertEqual(x['second'],4)


# from skydl.cython.examples.mcpp.test.container_unit_tests import (
#     run_emplace_object_move_vector,
#     run_emplace_object_move_map,
#     run_emplace_move_vector,
#     run_emplace_vector_unique_ptr,
#     run_emplace_vector,
#     run_emplace_object_pos_move_vector,
#     run_emplace_pos_move_vector_unique_ptr,
#     run_emplace_pos_move_vector_unique_ptr2,
#     run_push_back_move_vector,
#     run_push_front_move_list,
#     run_push_front_move_deque
# )

# class EmplaceTest(unittest.TestCase):
#     def test_emplace_object_move_vector(self):
#         x=run_emplace_object_move_vector()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_emplace_object_move_map(self):
#         x=run_emplace_object_move_map()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_emplace_move_vector(self):
#         x=run_emplace_move_vector()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_emplace_vector_unique_ptr(self):
#         x=run_emplace_vector_unique_ptr()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_emplace_vector(self):
#         x=run_emplace_vector()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#
# class EmplacePosTest(unittest.TestCase):
#     def test_emplace_object_pos_move_vector(self):
#         x = run_emplace_object_pos_move_vector()
#         self.assertEqual(x['size'],2)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_emplace_pos_move_vector_unique_ptr(self):
#         x = run_emplace_pos_move_vector_unique_ptr()
#         self.assertEqual(x['size'],2)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_emplace_pos_move_vector_unique_ptr2(self):
#         x = run_emplace_pos_move_vector_unique_ptr2()
#         self.assertEqual(x['size'],2)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#
# class PushBackTest(unittest.TestCase):
#     def test_push_back_move_vector(self):
#         x=run_push_back_move_vector()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#
# class PushFrontTest(unittest.TestCase):
#     def test_push_front_move_list(self):
#         x=run_push_front_move_list()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)
#     def test_push_front_move_deque(self):
#         x=run_push_front_move_deque()
#         self.assertEqual(x['size'],1)
#         self.assertEqual(x['first'],2)
#         self.assertEqual(x['second'],4)


