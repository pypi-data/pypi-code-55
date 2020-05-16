from logistic_module.LogisticEquation.Visualization import Visualization
from logistic_module.LogisticEquation.Bifurcation import Visualization_bifurcation
import time, tracemalloc
viz = Visualization()
bif = Visualization_bifurcation()

start = time.time()
tracemalloc.start()
viz.start_animation()
end = time.time()
print("Time ellapsed to excute animation : {0:.5f} s.".format(end - start))
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is : {current / 10**6}MB")

start = time.time()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is : {current / 10**6}MB")
bif.bifurcation_diagram()
end = time.time()
print("Time ellapsed to make bifurcation diagram : {0:.5f} s.".format(end - start))
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is : {current / 10**6}MB")
