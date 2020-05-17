import arkab.nlp as nlp
import arkab.tensorflow as tf
import arkab.torch as th
from arkab.data import Dataset

__all__ = ['nlp', 'th', 'th', 'Dataset', 'version']

with open('/Users/gawainx/PycharmProjects/Arkab/VERSION', 'r') as vh:
    version = vh.readline()
