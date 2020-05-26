#!/usr/bin/env python
import sys
sys.path.append("/omx") #This path will be bound to the nbx folder in run.sh
import numpy as np
from nbx.pspace import ParameterSpace


sweep_params = ParameterSpace({
	"x": range(5),
	"y": [0,1,2,4],
})


def print_args(arg_dict):
	print(f"**nbx**\nRunning Experiment...")
	for k,v in arg_dict.items():
		print(f"\t{k}: {v}")


def run_nb_experiment(task_id=0, results_dir=".", x=0, y=0, **kwargs):
	"""
	This is an auto-generated function 
	based on the jupyter notebook 

	> 
	
	Don't judge, it might look ugly.
	"""
	print_args(locals())


	#nbx

	#nbx

	

	

	

	z=0;

	

	# ...
	#nbx

	print("my results:", x, y, z)
	#nbx

	with open(f"{results_dir}/your_file.txt", "w") as f:

	    f.write("I will be written to: example_nbx_bundle/results/task_id/your_file.txt")

	    f.write(f"\n{task_id}")


	print("\n**nbx**\nExperiment finished.")
