class Layer:
    '''
    Abstract class with Layer definitions
    '''

    def __init__(self):
        pass

    def forward(self, x):
        pass

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        pass

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def optimize(self):
        pass