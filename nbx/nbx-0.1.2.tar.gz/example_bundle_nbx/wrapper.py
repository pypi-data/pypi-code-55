#!/usr/bin/env python
import os
from pathlib import Path
import argparse

from experiment import sweep_params, run_nb_experiment

parser = argparse.ArgumentParser(description='Wraps an experiment...')
parser.add_argument('--job-id', dest="job_id", default=0, type=int)
parser.add_argument('--task-id', dest="task_id", default=0, type=int)
parser.add_argument('--results-dir', dest="results_dir", default=Path(__file__).parent/'results', type=str)
args = parser.parse_args()


def print_args(arg_dict):
	print(f"**nbx**\nCalling main...")
	for k,v in arg_dict.items():
		print(f"\t{k}: {v}")


def main(job_id,
		 task_id,
		 results_dir):
	
	print_args(locals())

	t = task_id
	results_dir = Path(results_dir)/f'{t}'

	if not os.path.exists(results_dir):
		os.makedirs(results_dir)

	xargs = sweep_params[t-1]
	xargs.update({"task_id": t,
				  "results_dir": results_dir})

	run_nb_experiment(**xargs)

if __name__ == "__main__":
	main(**vars(args))