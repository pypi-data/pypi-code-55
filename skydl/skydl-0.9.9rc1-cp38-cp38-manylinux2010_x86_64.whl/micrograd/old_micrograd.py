import random


# The tiniest Autograd engine. It's so cute!
class Value:
    """ stores a single scalar value and its gradient """
    def __init__(self, data):
        self.data = data
        self.grad = 0
        self.backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)  # attempt to wrap if given an int/float/etc
        out = Value(self.data + other.data)

        def backward():
            self.grad += out.grad
            other.grad += out.grad
            self.backward()
            other.backward()

        out.backward = backward

        return out

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)  # attempt to wrap if given an int/float/etc
        out = Value(self.data * other.data)

        def backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
            self.backward()
            other.backward()

        out.backward = backward

        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    def relu(self):
        out = Value(0 if self.data < 0 else self.data)

        def backward():
            self.grad += (out.data > 0) * out.grad
            self.backward()

        out.backward = backward
        return out

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"


# A neural networks "library" :D on top of it! I'm dying
class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0


class Neuron(Module):

    def __init__(self, nin, nonlin=True):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(0)
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum([wi * xi for wi, xi in zip(self.w, x)], self.b)
        return act.relu() if self.nonlin else act

    def parameters(self):
        return self.w + [self.b]

    def __repr__(self):
        return f"{'ReLU' if self.nonlin else 'Linear'}Neuron({len(self.w)})"


class Layer(Module):

    def __init__(self, nin, nout, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

    def __repr__(self):
        return f"Layer of [{', '.join(str(n) for n in self.neurons)}]"


class MLP(Module):

    def __init__(self, nin, nouts):
        sz = [nin] + nouts
        self.layers = [Layer(sz[i], sz[i + 1], nonlin=i != len(nouts) - 1) for i in range(len(nouts))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def __repr__(self):
        return f"MLP of [{', '.join(str(layer) for layer in self.layers)}]"
