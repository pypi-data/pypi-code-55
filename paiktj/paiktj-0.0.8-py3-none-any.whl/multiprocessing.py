from multiprocessing import Pool


def my_pool(func, iterable, processes, verbose=True, verbose_option="number", print_end_option="\n"):
    """
    :param func:
    :param iterable:
    :param processes:
    :param verbose:
    :param verbose_option:
    :param print_end_option:
    :return:
    """
    if verbose:
        global __wrapper
        if verbose_option == "number":
            num = len(iterable)

            def __wrapper(i):
                print("Doing multiprocessing : index : ", i, "/", num, end=print_end_option)
                return func(iterable[i])

            pool = Pool(processes=processes)
            result = pool.map(__wrapper, range(num))
            pool.close()
            pool.join()
        else:
            def __wrapper(param):
                print("Doing multiprocessing : param : ", param, end=print_end_option)
                return func(param)

            pool = Pool(processes=processes)
            result = pool.map(__wrapper, iterable)
            pool.close()
            pool.join()
        return result
    else:
        pool = Pool(processes=processes)
        result = pool.map(func, iterable)
        pool.close()
        pool.join()
        return result
