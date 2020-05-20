from .inputfile_creation import inputfile
class input_opt(inputfile):
    """ Generating inputfiles for geometry optimization calculations. 
    
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
    
    def opt_freq(self):
        """Function to define the optimization condition.
        
        Args: 
            Input scf condition from user
        
        Returns: 
            None
        """
        
        scf=input("\ndefine your scf procedure (type none to set up defaut scf=tight): ")
        if scf=="none":
            self.level = self.level + " opt freq"
        else:
            self.level = self.level + " opt freq " + scf
    