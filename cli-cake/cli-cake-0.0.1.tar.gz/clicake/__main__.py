from . import runnable
if __name__ == '__main__': # only run if invoked directly
    # Utitility runner that invokes a script
    @runnable
    def echo(*args):
        print(' '.join(args))
    echo()

    
    # scripts = {
    #     'sum_example': lambda *args: print(sum([int(a) for a in args]))
    # }
    # if sys.argv[1] in scripts:
    #     runnable(args=sys.argv[2:])(scripts[sys.argv[1]])()
    # else:
    #     print('Unknown command. Exiting...')