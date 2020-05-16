import numpy as np

class Model():
    
    def __init__(self, layers):
        self.layers = layers

    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        for layer in self.layers:
            y = layer(x)
            x = y
        return y
    
    def backward(self, dL):
        for layer in reversed(self.layers):
            dL = layer.backward(dL)
        return dL
    
    def optimize(self):
        for layer in self.layers:
            layer.optimize()

    def set_optimizer(self, optimizer):
        for layer in self.layers:
            layer.set_optimizer(optimizer)

    def set_loss(self, loss_fn):
        self.loss_fn = loss_fn

    def setup(self, loss_fn, optimizer):
        self.set_loss(loss_fn)
        self.set_optimizer(optimizer)

    def train(self, x_train, y_train, x_test=None, y_test=None, split=0.2, epochs=100, batch_size=10, lr=5e-3, verbose=1):
        steps = x_train.shape[0]//batch_size
        loss,accuracy = [],[]
        for epoch in range(epochs):
            epoch_loss = 0
            for i in range(0, x_train.shape[0], batch_size):
                x, y = x_train[i:i+batch_size], y_train[i:i+batch_size]
                y_pred = self.forward(x)

                epoch_loss += self.loss_fn(y, y_pred)
                
                dL_dy = self.loss_fn.gradient()

                self.backward(dL_dy)

                self.optimize()
            epoch_loss_test = epoch_loss/steps
            loss.append(epoch_loss_test)
            if x_test is not None:
                accuracy.append(self.evaluate_accuracy(x_test, y_test))
            
            if verbose == 1:
                print("Epoch {} training loss = {}".format(epoch, epoch_loss_test) )
        self.loss = loss
        self.accuracy = accuracy
        return loss,accuracy

    def predict(self, x):
        estimate = self.forward(x)
        return estimate

    def evaluate_accuracy(self, x_val, y_val):
        num_corrects = 0
        for i in range(x_val.shape[0]):
            if self.predict(x_val) == y_val:
                num_corrects += 1
        return num_corrects/x_val.shape[0]