from time import time


def time_fun(problem, funct):
    problem.start_time = time()
    solution = funct(problem)
    problem.add_solution(solution)
