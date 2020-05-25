import sys, logging
from io import StringIO

def reroute(func, *args):
    '''
    Reroute standard output during an individual function,
    and return the outputs.
    '''
    stdout = sys.stdout = StringIO()
    stderr = sys.stderr = StringIO()
    func(*args)
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    return stdout.getvalue(), stderr.getvalue()

class OutputController:

    def __init__(self):
        self.stdout = []
        self.stderr = []

    def open(self):
        '''
        Append an object to our outputs list that output
        will now be piped to.
        '''
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        self.stdout.append(sys.stdout)
        self.stderr.append(sys.stderr)
        

    def close(self):
        '''
        Pop from the outputs list, return the outputs as strings.
        Begin piping to the next object in the outputs list.
        '''
        tstdout = ''
        tstderr = ''
        if self.stdout and self.stderr:
#            logging.info([x for x in self.stdout])
            #If the stack is not empty, save the outputs to variables that will be returned at the end of this function.
            tstdout = self.stdout.pop().getvalue()
            tstderr = self.stderr.pop().getvalue()
            logging.debug('Standard output:\t%s\tStandard error:\t%s'%(tstdout, tstderr))
            
            if self.stdout and self.stderr:
                #If the stack is not empty, then pipe output to the next object in the stack.
                sys.stdout = self.stdout[-1]
                sys.stderr = self.stderr[-1]
            else:
                #If the stack is empty, reset output to default.
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
        else:
            logging.info('The output stack is empty, please open a new output to add to the stack.')
        return tstdout, tstderr 
    
    def pclose(self):
        '''
        Run the close function, logging.info its output
        '''
        logging.info('stdout\n------------\n%s\nstderr\n----------\n%s'%self.close())
