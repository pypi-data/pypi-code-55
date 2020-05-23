import os,warnings,sys
import numpy as np
import traceback
import multiprocessing
from multiprocessing import Pool
try:
    import cPickle as pick
except:
    import pickle as pick

__all__=['foreach','parReturn']

def foreach(toPar,parFunc,args=None,numThreads=multiprocessing.cpu_count()):
    """Main pyParz function.

    Parameters
    ----------
    toPar: :class:`~list` or :class:`~numpy.ndarray`
            The list of things to be parallelized.
    parFunc: function
            The function that each element of toPar is passed to.
    args: :class:`~list`
            The list of arguments to be passed to each iteration.
    numTreads: int
            The number of cores you want to use.

    Returns
    -------
    results: :class:`~list`
            The list of results in arbitrary order
    """


    results=[]
    p = Pool(processes=numThreads)
    if args is not None:
        if isinstance(toPar[0],(list,tuple,np.ndarray)):
            for x in p.imap_unordered(_parWrap,[[parFunc,[y,args]] for y in toPar]):
                results.append(x)
        else:
            for x in p.imap_unordered(_parWrap,[[parFunc,np.append(y,args)] for y in toPar]):
                results.append(x)
        p.close()
    else:
        
        for x in p.imap_unordered(_parWrap,[[parFunc,y] for y in toPar]):
            results.append(x)
        p.close()

    return results

def _parWrap(args):
    func,newArgs=args
    
    try:
        return(func(newArgs))
    except Exception as e:
        print('Failed')
        return(traceback.format_exc())

def _pickleable(obj):
    try:
        with open(r"temp.pickle", "wb") as output_file:
            pick.dump(obj, output_file)
        pickle=True
    except:
        pickle=False
    try:
        os.remove('temp.pickle')
    except:
        pass
    return pickle

def parReturn(toReturn):
    """Optional return function.

    Parameters
    ----------
    toReturn: :class:`~list` or :class:`~np.ndarray` or :class:`~dict`
            Item to return
    Returns
    -------
    final:
        Returns pickleable elements.
    """ 
    if isinstance(toReturn,dict):
        final=dict([])
        for key in toReturn:
            if _pickleable(toReturn[key]):
                final[key]=toReturn[key]
            else:
                print("Had to remove object %s from return dictionary, as it was not pickleable."%key)

    elif isinstance(toReturn,(tuple,list,np.ndarray)):
        final=[]
        for i in range(len(toReturn)):
            if _pickleable(toReturn[i]):
                final.append(toReturn[i])
            else:
                print("Had to remove the %i (th) object from return array, as it was not pickleable."%i)
    else:
        print('I do not recognize the data type of your return variable')
        sys.exit()

    if final:
        return final
    else:
        print('Nothing you wanted to return was Pickleable')
        sys.exit()

