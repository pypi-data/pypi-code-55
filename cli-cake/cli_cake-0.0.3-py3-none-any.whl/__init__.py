import sys
from functools import wraps
def runnable(
    _func = None,
    args = sys.argv[1:],
    print_output=True
    ):
    '''
        decorator for making scripts CLI callable.
        Returns a method that looks up CLI args and invokes
        function when called.
        Positional arguments are set just by listing the args in order,
        named arguments can be specified by using the flag with
        the same name as the arg prepended by -- (i.e. an arg called "file"
        could be set by `--file examplefilename.txt`)
    '''
    def _runnable(callback):
        def cast_arg(arg):
            def custom_cast(b):
                if b == 'True':
                    return True
                if b == 'False':
                    return False
                if b == 'None':
                    return None
                raise ValueError('Not Boolean')
            for cast in (custom_cast, int, float):
                try:
                    return cast(arg)
                except ValueError:
                    pass
            return arg
        @wraps(callback)
        def run_callback(
            args = args,
            print_output=print_output
        ):
            # args = parser.parse_args()
            curr_arg='_args'
            parsed_args={'_args': []}
            curr_arg_values = []
            def update_args(new_curr_arg):
                nonlocal curr_arg
                nonlocal curr_arg_values
                if curr_arg == '_args':
                    pass
                elif len(curr_arg_values) == 0:
                    parsed_args[curr_arg] = True
                elif len(curr_arg_values) == 1:
                    parsed_args[curr_arg] = curr_arg_values[0]
                else:
                    parsed_args[curr_arg] = curr_arg_values
                curr_arg = new_curr_arg.strip('-')
                curr_arg_values = []
            for arg in args:
                if arg.startswith(('-','--')):
                    update_args(arg)
                else:
                    arg = cast_arg(arg)
                    if curr_arg == '_args':
                        parsed_args['_args'].append(arg)
                    else:
                        curr_arg_values.append(arg)
            update_args('')

            pargs = parsed_args['_args']
            del parsed_args['_args']
            output = callback(*pargs,**parsed_args)
            if print_output:
                print(output)
            return output
        callback.runCLI = run_callback
        return callback
        # return run_callback

    if callable(_func): # If the first positional argument passed is a function,
        # then don't return decorator, just return decorated function
        # allows for decorator to be called like
        # @runnable
        # or 
        # @runnable() for when we want to pass in additional stuff
        return _runnable(_func)
    return _runnable

def run(callback, **kwargs):
    """
    Locally wraps the callback with a runnable() decorator
    and runs it. Can pass same optional args here as you can
    to runnable
    """
    return runnable(**kwargs)(callback).runCLI()

class Cake:
    """
    Wrapper for multi-method support
    """
    def __init__(self):
        self.methods = {}
    def runnable(self, method, name=None, **kwargs):
        """
        Adds the specified method to parser.
        args keyword can't be set.
        use name to override default function name
        acts as standard runnable otherwise (can be invoked directly)
        """
        if name == None:
            name = method.__name__
        if 'args' in kwargs:
            raise ValueError("args: Can't set custom args for Cake runnable")
        if name in self.methods:
            raise ValueError(f"Function with name {name} already registered")
        self.methods[name] = runnable(**kwargs)(method)
        return self.methods[name]
    def run(self):
        """
        First non-name CLI arg is parsed to choose which method to run, and then that
        method is run.
        """
        if sys.argv[1] in self.methods:
            self.methods[sys.argv[1]].runCLI(args=sys.argv[2:])
        else:
            raise ValueError(f"Unknown method {sys.argv[1]}")