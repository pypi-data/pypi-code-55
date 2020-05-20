class inputfile:
    
    def __init__(self, a = 0, b = 1, memory='16gb', cpu=4, level_of_theory= 'B3LYP/6-31+G(d) EmpiricalDispersion=GD3', name='default.com'):
        """ Generic class for generating inputfiles for various calculations. 
    
        Attributes:
            charge (float) define the charge of system
            multiplicity (float) define the multiplicity of system
            memory (string) requested memory for calculation
            cpu (float) requested cpu for calculation
            level (string) defined the calculation condition
            name (string) defined the name of inputfile
            coordinate (list or string) a list or string of molecule coordinates
        """
        self.charge = a
        self.multiplicity = b
        self.memory = memory
        self.cpu = cpu
        self.level = level_of_theory
        self.name = name
        self.coordinate = []
    
    def input_condition(self):
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
        
        b3lyp=["b3lyp-d3", "B3LYP-D3", "b3lyp-D3", "B3LYP-d3", "B3lyp-d3", "B3lyp-D3"]
        functional = input("\nSpecify the funtional of calculation: ")
        basis = input("\nSpecify the basis set: ")
        if any(x in functional for x in b3lyp):
            self.level = "B3LYP/{} EmpiricalDispersion=GD3".format(basis)
        else:
            self.level = "{}/{}".format(functional,basis)
                
    def input_coordinate(self):
        """Function to read coordinate (string) from user input.
        
        Args:
            None
        
        Returns:
            None
        
        """
        print("\nInput the coordinate of your molecule, double hit enter to finish")
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        self.coordinate = '\n'.join(lines)
    
    def generate_inputfile(self):
        """Function to generate the inputfile for various calculation.
        
        Args: 
            None
        
        Returns: 
            com file: preparied input file
    
        """
        f = open("{}.com".format(self.name),'w')
        f.write("$RunGauss\n%NprocLinda=1\n%Mem={}gb\n%NProcshared={}\n# {}\n\nTest\n\n{},{}\n{}\n".format(self.memory, self.cpu, self.level, self.charge, self.multiplicity, self.coordinate))