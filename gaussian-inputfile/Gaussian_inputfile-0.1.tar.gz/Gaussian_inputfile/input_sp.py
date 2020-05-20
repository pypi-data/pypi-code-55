from .inputfile_creation import inputfile
class input_sp(inputfile):
    """ Generating inputfiles for single-point calculations. 
    
        Attributes:
            charge (float) define the charge of system
            multiplicity (float) define the multiplicity of system
            memory (string) requested memory for calculation
            cpu (float) requested cpu for calculation
            level (string) defined the calculation condition
            name (string) defined the name of inputfile
            coordinate (list or string) a list or string of molecule coordinates
    """
    def __init__(self):
        inputfile.__init__(self)
    