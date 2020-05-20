from .inputfile_creation import inputfile
class input_nics(inputfile):
    """ Generating inputfiles for nics calculations. 
    
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
    
    def nics_condition(self):
        """ Define the basic information for input file. 
    
            Attributes:
            charge (float) define the charge of system
            multiplicity (float) define the multiplicity of system
            memory (string) requested memory for calculation
            cpu (float) requested cpu for calculation
            level (string) defined the level of theory
            name (string) defined the name of inputfile
        """
        self.charge = input("\nWhat's the charge of system? ")
        self.multiplicity = input("\nWhat's the multiplicity of system? ")
        self.name = input("\nType in the name of your inputfile: ")
        ans = input("\nChoose CPU&Mem: a. 4cpu+16gb b. 8cpu+32gb ")
        if ans == "a":
            self.cpu, self.memory = 4,'16gb'
        elif ans == "b":
            self.cpu, self.memory = 8,'32gb'
        
        self.level = " PW91PW91/gen NMR pop=(full) IOp(10/46=1) Gfprint"
    def nics_basis_set(self):
        """Function to read basis set for NICS calculation.
        
        Args:
            None
        
        Returns:
            None
        
        """
        print("Input the basis set (IGLOIII) for your molecule:\nsee https://www.basissetexchange.org, hit enter to finish")
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        basis_set = '\n'.join(lines)
        self.coordinate = self.coordinate + "\n\n" + basis_set
        