from .inputfile_creation import inputfile
class input_nbo(inputfile):
    """ Generating inputfiles for nbo calculations. 
    
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
    
    def nbo_condition(self):
        """Function to define the NBO calculation condition.
        
        Args: 
            User input NBO keyword
        
        Returns: 
            None
        """
        nbo=input("\nChoose your NBO keyword:\n\nNBOSUM: requests printing NBO summary table" \
        "\nResonance: requests search for highly delocalized strucuture" \
        "\n3CBOND: requests search for 3-center bonds" \
        "\nNLMO: computes and print out the summary of NLMOs" \
        "\nBNDIDX: calculates and print Wiberg bond indices\n")
        
        nbo = "\n\n$NBO " + nbo + " $END"
        self.level = self.level + " pop=nbo7read"
        self.coordinate = self.coordinate + nbo
    