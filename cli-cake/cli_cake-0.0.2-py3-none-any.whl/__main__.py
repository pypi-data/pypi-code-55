from . import runnable
if __name__ == '__main__': # only run if invoked directly
    # example script
    @runnable
    def echo(*args):
        print(' '.join(args))
    echo()