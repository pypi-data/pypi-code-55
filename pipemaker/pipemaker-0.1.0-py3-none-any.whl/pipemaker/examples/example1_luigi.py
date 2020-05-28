import luigi
import pickle
from . import example1


class Make_odd(luigi.Task):
    low = luigi.IntParameter()
    delay = luigi.IntParameter(default=2)
    path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f"{self.path}/odd.pkl")

    def run(self):
        r = example1.make_odd(self.low, self.delay)
        self.output().makedirs()
        with self.output().temporary_path() as f:
            pickle.dump(r, open(f, "wb"))


class Make_even(luigi.Task):
    low = luigi.IntParameter()
    delay = luigi.IntParameter(default=5)
    path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f"{self.path}/even.pkl")

    def run(self):
        r = example1.make_even(self.low, self.delay)
        self.output().makedirs()
        with self.output().temporary_path() as f:
            pickle.dump(r, open(f, "wb"))


class Make_oddeven(luigi.Task):
    low = luigi.IntParameter()
    delay = luigi.IntParameter(default=8)
    path = luigi.Parameter()

    def requires(self):
        return dict(
            odd=Make_odd(self.low, self.delay, self.path),
            even=Make_even(self.low, self.delay, self.path),
        )

    def output(self):
        return luigi.LocalTarget(f"{self.path}/oddeven.pkl")

    def run(self):
        odd = pickle.load(open(self.input()["odd"].path, "rb"))
        even = pickle.load(open(self.input()["even"].path, "rb"))
        r = example1.make_oddeven(odd, even)
        self.output().makedirs()
        with self.output().temporary_path() as f:
            pickle.dump(r, open(f, "wb"))
