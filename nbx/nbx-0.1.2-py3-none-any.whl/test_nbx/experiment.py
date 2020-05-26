#!/usr/bin/env python
import fire
import sys
sys.path.append("/omx") #This path will be bound to the nbx folder in run.sh
import numpy as np
from nbx.pspace import ParameterSpace


sweep_params = ParameterSpace({
	"y": [0,1,2,3,4],
})


def print_args(arg_dict):
	print(f"**nbx**\nRunning Experiment...")
	for k,v in arg_dict.items():
		print(f"\t{k}: {v}")


def run_nb_experiment(task_id=0, results_dir="./", x=0, y=0, **kwargs):
	"""
	This is an auto-generated function 
	based on the jupyter notebook 

	> 
	
	Don't judge, it might look ugly.
	"""
	print_args(locals())


	#nbx

	

	

	

	z=0;
	#nbx

	print("my results:", x, y, z)


	print("\n**nbx**\nExperiment finished.")


if __name__ == '__main__': 
	fire.Fire(run_nb_experiment)