import os
import unittest
from diarypy.diary import Diary

class TestDiary(unittest.TestCase):
    def setUp(self):
        self.diary = Diary(name='test_diary', path='unittest_folder',
                           overwrite=True, stdout=False, stderr=False)

    def test_diary_exists(self):
        assert(os.path.exists(self.diary.path))

    def test_add_notebook(self):

        self.diary.add_notebook('test1')

        self.diary.add_entry('test1', ['abc', 123, 'abc'])

        assert(os.path.exists(os.path.join(self.diary.path,
                       self.diary.notebooks['test1'].filename)))

    def test_notebook_instance(self):
        notebook = self.diary.add_notebook('test2')

        notebook.add_entry(['a', 1])
        notebook.add_entry(['b', 2])
        notebook.add_entry(['c', 3])

        assert(os.path.exists(os.path.join(self.diary.path,
                                           notebook.filename)))

    def test_notebook_history(self):
        notebook = self.diary.add_notebook('test3')

        rows = [['a', 1], [2, 'ab'], ['abc', 3]]

        for row in rows:
            notebook.add_entry(row)

        for row, hist in zip(rows, notebook.history):
            for a, b in zip(row, hist[4:]):
                assert(a == b)

    def test_load_diary(self):
        diary1 = Diary(name='load_test', path='unittest_folder',
                       overwrite=True, stdout=False, stderr=False)
        diary1.add_notebook('test1')

        rows = [['a', 'a'], ['b', 'b'], ['c', 'c']]
        for row in rows:
            diary1.add_entry('test1', row)

        diary2 = Diary(name=None, path=diary1.path)

        for row, hist in zip(rows, diary2.notebooks['test1'].history):
            for a, b in zip(row, hist[4:]):
                assert(a == b)

    def test_stdout(self):
        diary = Diary(name='test_stdout', path='unittest_folder',
                      overwrite=True, stdout=True, stderr=False)
        stdout_file = os.path.join(diary.path, 'stdout.txt')
        sentence_list = ['This is an stdout example',
                         'and this is the second line']
        for sentence in sentence_list:
            print(sentence)
        del diary

        assert(os.path.exists(stdout_file))

        with open(stdout_file, 'r') as f:
            for sentence, line in zip(sentence_list, f.readlines()):
                assert(sentence == line.rstrip())

def main():
    unittest.main()


if __name__ == '__main__':
    main()
