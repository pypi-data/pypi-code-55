import numpy as np
import matplotlib.pyplot as plt
epsilon = 1e-7 # global variable for fixing nan issues caused.

class Activation_Functions:


  def sigmoid(self,Z):
    A = 1/(1+np.exp(-Z))
    return A


  def tanh(self,Z):
    A = np.tanh(Z)
    return A


  def relu(self,Z):
    A = np.maximum(0,Z)
    return A


  def softmax(self,Z):
    A = np.exp(Z)/(np.sum(np.exp(Z))+epsilon)
    return A


  def relu_backward(self,dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True) 
    dZ[Z <= 0] = 0
    return dZ


  def sigmoid_backward(self,dA, cache):
    Z = cache
    s = 1/(1+np.exp(-Z))
    dZ = dA * s * (1-s)
    return dZ


  def tanh_backward(self,dA, cache):
    A = cache
    dZ = np.multiply(dA, 1 - np.power(A, 2))
    return dZ

  def softmax_backward(self,dA,cache):
    Z = cache
    global epsilon
    Z = np.exp(Z)
    numerator = np.multiply( Z , np.sum(Z,axis=0,keepdims=True) - Z )
    denominator = np.square(np.sum(Z,axis=0,keepdims=True))+epsilon
    dZ = np.divide(numerator,denominator)
    return dZ

class Weight_Initialization:

  def weight_initialize_randomize(self,curr_layer,prev_layer,random_initializer):

    W = np.random.randn(curr_layer,prev_layer) * random_initializer
    b = np.zeros((curr_layer,1))
    return W,b

  def weight_initialize_xavier(self,curr_layer,prev_layer):

    W = np.random.randn(curr_layer,prev_layer) * np.sqrt(2/(curr_layer+prev_layer))
    b = np.zeros((curr_layer,1))
    return W,b

  def weight_initialize_he(self,curr_layer,prev_layer):
    
    W = np.random.randn(curr_layer, prev_layer) / np.sqrt(prev_layer) #np.random.randn(curr_layer,prev_layer) * np.sqrt(2/(prev_layer))
    b = np.zeros((curr_layer,1))
    return W,b

class Regularization_Functions:

  def cost_L1(self,W,reg_lambda):
    regularizer_cost = reg_lambda * np.sum(np.absolute(W))
    return regularizer_cost

  def cost_L2(self,W,reg_lambda):
    regularizer_cost = reg_lambda * np.sum(np.square(W))
    return regularizer_cost


  def compute_regularizer_cost(self,m,parameters,regularizer_layers):
    regularizer_compute_cost = 0
    for i in regularizer_layers:
      W = parameters["W"+i[1]]
      reg_lambda = regularizer_layers[i][1]
      if regularizer_layers[i][0] == "L1":
        regularizer_compute_cost += self.cost_L1(W,reg_lambda)
      elif regularizer_layers[i][0] == "L2":
        regularizer_compute_cost += self.cost_L2(W,reg_lambda)

    regularizer_compute_cost = regularizer_compute_cost/(2*m)
    return regularizer_compute_cost


  def backward_propagation_L1(self,W,m,reg_lambda):
    return reg_lambda/(2*m)


  def backward_propagation_L2(self,W,m,reg_lambda):
    return reg_lambda*W/m


  def backward_propagation_regularizer(self,m,parameters,regularizer_layers):
    grads_regularizers = {}
    for i in regularizer_layers:
      W = parameters["W"+i[1]]
      reg_lambda = regularizer_layers[i][1]
      if regularizer_layers[i][0] == "L1":
        grads_regularizers["dW"+i[1]] = self.backward_propagation_L1(W,m,reg_lambda)
      elif regularizer_layers[i][0] == "L2":
        grads_regularizers["dW"+i[1]] = self.backward_propagation_L2(W,m,reg_lambda)
      
    return grads_regularizers

class Drop_Out:

  def inverted_dropout_cache(self,A,dropout):

      D = np.random.randn(A.shape[0],A.shape[1]) < dropout
      A = A * D
      A = A / dropout
      
      return A,D

  def inverted_dropout_grads(self,dA,D,dropout):

    dA = dA * D
    dA = dA / dropout

    return dA

class Optimizers:

  def initialize_momentum(self,parameters,total_layers):

    v = {}
    for i in range(1,total_layers):
      v["dW" + str(i)] = np.zeros(parameters["W" + str(i)].shape)
      v["db" + str(i)] = np.zeros(parameters["b" + str(i)].shape)

    return v


  def initialize_rmsProp(self,parameters,total_layers):

    s = {}
    for i in range(1,total_layers):
      s["dW" + str(i)] = np.zeros(parameters["W" + str(i)].shape)
      s["db" + str(i)] = np.zeros(parameters["b" + str(i)].shape)

    return s


  def initialize_adam(self,parameters,total_layers):

    v = {}
    s = {}

    v = self.initialize_momentum(parameters,total_layers)
    s = self.initialize_rmsProp(parameters,total_layers)

    return v,s


  def gradient(self,parameters,total_layers,learning_rate,grads):

    for l in range(1,total_layers):
      parameters["W" + str(l)] = parameters["W" + str(l)] - learning_rate*grads["dW"+str(l)]
      parameters["b" + str(l)] = parameters["b" + str(l)] - learning_rate*grads["db"+str(l)]
    
    return parameters


  def momentum(self,parameters,v,total_layers,learning_rate,grads,beta):


    for l in range(1,total_layers):
      v["dW" + str(l)] = beta * v["dW" + str(l)] + (1 - beta) * grads['dW' + str(l)]
      v["db" + str(l)] = beta * v["db" + str(l)] + (1 - beta) * grads['db' + str(l)]
      parameters["W" + str(l)] = parameters["W" + str(l)] - learning_rate * v["dW" + str(l)]
      parameters["b" + str(l)] = parameters["b" + str(l)] - learning_rate * v["db" + str(l)]
    
    return parameters


  def rmsProp(self,parameters,s,total_layers,learning_rate,grads,beta):
    global epsilon
    for l in range(1,total_layers):
      s["dW" + str(l)] = beta * s["dW" + str(l)] + (1 - beta) * np.square(grads['dW' + str(l)])
      s["db" + str(l)] = beta * s["db" + str(l)] + (1 - beta) * np.square(grads['db' + str(l)])
      parameters["W" + str(l)] = parameters["W" + str(l)] - learning_rate * np.divide(grads["dW" + str(l)],np.sqrt(s["dW" + str(l)])+epsilon)
      parameters["b" + str(l)] = parameters["b" + str(l)] - learning_rate * np.divide(grads["db" + str(l)],np.sqrt(s["db" + str(l)])+epsilon)

    return parameters


  def adam(self,parameters,v,s,t,total_layers,learning_rate,grads,beta1,beta2):
    v_corrected = {}
    s_corrected = {}
    epsilon = 1e-8        

    for l in range(1,total_layers):
      v["dW" + str(l)] = beta1 * v["dW" + str(l)] + (1 - beta1) * grads['dW' + str(l)]
      v["db" + str(l)] = beta1 * v["db" + str(l)] + (1 - beta1) * grads['db' + str(l)]
      
      v_corrected["dW" + str(l)] = v["dW" + str(l)] / (1 - np.power(beta1, t))
      v_corrected["db" + str(l)] = v["db" + str(l)] / (1 - np.power(beta1, t))

      s["dW" + str(l)] = beta2 * s["dW" + str(l)] + (1 - beta2) * np.power(grads['dW' + str(l)], 2)
      s["db" + str(l)] = beta2 * s["db" + str(l)] + (1 - beta2) * np.power(grads['db' + str(l)], 2)

      s_corrected["dW" + str(l)] = s["dW" + str(l)] / (1 - np.power(beta2, t))
      s_corrected["db" + str(l)] = s["db" + str(l)] / (1 - np.power(beta2, t))

      parameters["W" + str(l)] = parameters["W" + str(l)] - learning_rate * v_corrected["dW" + str(l)] / np.sqrt(s_corrected["dW" + str(l)] + epsilon)
      parameters["b" + str(l)] = parameters["b" + str(l)] - learning_rate * v_corrected["db" + str(l)] / np.sqrt(s_corrected["db" + str(l)] + epsilon)


    return parameters

class Cost_Functions:

  def crossEntropy_cost(self,Y_pred,Y,m):

    cost = (1./m) * (-np.dot(Y,np.log(Y_pred).T) - np.dot(1-Y, np.log(1-Y_pred).T))
    return cost

  def meanSquare_cost(self,Y_pred,Y,m):

    cost = (1/m) * np.sum(np.square(Y - Y_pred))
    return cost

  def crossEntropy_derivative(self,Y_pred,Y):

    dA = -(np.divide(Y, Y_pred+epsilon) - np.divide(1 - Y, 1 - Y_pred+epsilon))
    return dA 

  def meanSquare_derivative(self,Y_pred,Y):

    dA = Y_pred - Y
    return dA

  def categorical_crossEntropy_cost(self,Y_pred,Y,m):

    cost = (-1 / m) * np.sum(np.multiply(Y, np.log(Y_pred+epsilon)))
    return cost

  def categorical_crossEntropy_derivative(self,Y_pred,Y):

    dA = -np.divide(Y,Y_pred+epsilon)
    return dA

def generate_mini_batches(X, Y, batch_size = 64):

    m = X.shape[1]                  
    mini_batches = []
        

    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation].reshape((Y.shape[0],m))


    num_complete_minibatches = int(np.floor(m/batch_size)) 

    for k in range(num_complete_minibatches):
        mini_batch_X = shuffled_X[:,k * batch_size:(k + 1) * batch_size]
        mini_batch_Y = shuffled_Y[:,k * batch_size:(k + 1) * batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    

    if m % batch_size != 0:
        mini_batch_X = shuffled_X[:,num_complete_minibatches *batch_size:]
        mini_batch_Y = shuffled_Y[:,num_complete_minibatches * batch_size:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
        num_complete_minibatches += 1
    
    return mini_batches,num_complete_minibatches

def forward_propagation(X,total_layers,parameters,activations,dropout_layers):

  cache = {}
  cache["A0"] = X

  activation_function = Activation_Functions()
  drop_out = Drop_Out()

  for i in range(1,total_layers):
    
    cache["Z" + str(i)] = np.dot(parameters["W" + str(i)],cache["A"+str(i-1)]) + parameters["b" + str(i)]

    if activations["AF"+str(i)] == "sigmoid":
      cache["A" + str(i)] = activation_function.sigmoid(cache["Z" + str(i)])

    elif activations["AF"+str(i)] == "tanh":
      cache["A" + str(i)] = activation_function.tanh(cache["Z" + str(i)])

    elif activations["AF"+str(i)] == "relu":
      cache["A" + str(i)] = activation_function.relu(cache["Z" + str(i)])

    elif activations["AF"+str(i)] == "softmax":
      cache["A" + str(i)] = activation_function.softmax(cache["Z" + str(i)])


    if "h" + str(i) in dropout_layers.keys():
      cache["A" + str(i)],cache["D" + str(i)] = drop_out.inverted_dropout_cache(cache["A" + str(i)],dropout_layers["h" + str(i)])

  return cache

def compute_cost(Y_pred,Y,cost_function,parameters,regularizer_layers):

  regularization_function = Regularization_Functions()
  cost_functions = Cost_Functions()
  
  m = Y.shape[1]
  reg_cost = regularization_function.compute_regularizer_cost(m,parameters,regularizer_layers)

  if cost_function == "crossEntropy":
    cost = cost_functions.crossEntropy_cost(Y_pred,Y,m)

  elif cost_function == "meanSquare":
    cost = cost_functions.meanSquare_cost(Y_pred,Y,m)

  elif cost_function == "categoricalCrossEntropy":
    cost = cost_functions.categorical_crossEntropy_cost(Y_pred,Y,m)


  cost = cost + reg_cost
  cost = np.squeeze(cost)
  
  return cost

def backward_propagation(Y,cost_function,parameters,cache,activations,total_layers,regularizer_layers,dropout_layers):

  Y_pred = cache["A" + str(total_layers)]
  m = Y_pred.shape[1]
  Y = Y.reshape(Y_pred.shape)
  grads = {}
  propogate = {} 
  
  activation_function = Activation_Functions()
  cost_functions = Cost_Functions()
  drop_out = Drop_Out()
  regularization_function = Regularization_Functions()

  if cost_function == "crossEntropy":
    propogate["dA"+str(total_layers)] = cost_functions.crossEntropy_derivative(Y_pred,Y)  

  elif cost_function == "meanSquare":
    propogate["dA"+str(total_layers)] = cost_functions.meanSquare_derivative(Y_pred,Y)

  elif cost_function == "categoricalCrossEntropy":
    propogate["dA"+str(total_layers)] = cost_functions.categorical_crossEntropy_derivative(Y_pred,Y)


  for i in range(total_layers,0,-1):

    if (activations["AF" + str(i)] == "sigmoid"):
      propogate["dZ"+str(i)] = activation_function.sigmoid_backward(propogate["dA"+str(i)], cache["Z" + str(i)])

    elif (activations["AF" + str(i)] == "relu"):
      propogate["dZ"+str(i)] = activation_function.relu_backward(propogate["dA"+str(i)], cache["Z" + str(i)])

    elif (activations["AF" + str(i)] == "tanh"):
      propogate["dZ"+str(i)] = activation_function.tanh_backward(propogate["dA"+str(i)], cache["A" + str(i)])

    elif (activations["AF" + str(i)] == "softmax"):
      propogate["dZ"+str(i)] = activation_function.softmax_backward(propogate["dA"+str(i)], cache["Z" + str(i)])

    grads["dW"+str(i)] = (1 / m) * np.dot(propogate["dZ"+str(i)], cache["A"+str(i-1)].T)

    grads["db"+str(i)] = (1 / m) * np.sum(propogate["dZ"+str(i)], axis=1, keepdims=True)

    propogate["dA"+str(i-1)] = np.dot(parameters["W"+str(i)].T,propogate["dZ"+str(i)])

    if "D"+str(i-1) in  cache.keys():
      propogate["dA"+str(i-1)] = drop_out.inverted_dropout_grads(propogate["dA"+str(i-1)],cache["D"+str(i-1)],dropout_layers["h"+str(i-1)])
  
  

  grads_regularizers = regularization_function.backward_propagation_regularizer(m,parameters,regularizer_layers)
  for i in grads_regularizers:
    grads[i] += grads_regularizers[i]
    
  return grads

def update_parameters(parameters,v,s,t,grads,learning_rate,total_layers,optimizer,momentum_beta,rms_beta,adam_beta1,adam_beta2):

  optimizers = Optimizers()

  if optimizer == "gradient":
    parameters = optimizers.gradient(parameters,total_layers,learning_rate,grads)
    
  elif optimizer == "momentum":
    parameters = optimizers.momentum(parameters,v,total_layers,learning_rate,grads,momentum_beta)

  elif optimizer == "rmsProp":
    parameters = optimizers.rmsProp(parameters,s,total_layers,learning_rate,grads,rms_beta)

  elif optimizer == "adam":
    parameters = optimizers.adam(parameters,v,s,t,total_layers,learning_rate,grads,adam_beta1,adam_beta2)

  return parameters

class Architecture:



  def __init__(self):

    self.parameters = {}
    self.activations = {}
    self.cache = {}
    self.grads = {}
    self.layer_dims = []
    self.total_layers = 0
    self.cost_function = ''
    self.optimizer = ''
    self.learning_rate = 0
    self.momentum_beta = 0
    self.rms_beta = 0
    self.adam_beta1 = 0
    self.adam_beta2 = 0
    self.adam_t = 0
    self.cost = 0
    self.cost_graph = []
    self.weight_initialization = ''
    self.random_initializer = 0
    self.regularizer_layers = {}
    self.dropout_layers = {}
    self.momentum_parameters = {}
    self.rms_parameters = {}
    self.batch_size = 0
    self.mini_batches = []
    self.mini_iterations = 0
    self.input_mean = 0
    self.input_variance = 0

  def add_inputLayer(self,input_units,normalization = False,weight_initialization="randomize",random_initializer = 0.01):

    self.normalization = normalization
    self.layer_dims.append(input_units)
    self.total_layers += 1
    self.weight_initialization = weight_initialization
    self.random_initializer = random_initializer
    #np.random.seed(1)





  def add_hiddenLayer(self,hidden_units, activation_function = "sigmoid", dropout = 1,regularizer = None, regularizer_lambda=0.1):

    weight_initializer = Weight_Initialization()

    if (regularizer != None):
      self.regularizer_layers["h"+str(self.total_layers)] = (regularizer,regularizer_lambda)

    if dropout < 1:
      self.dropout_layers["h" + str(self.total_layers)] = dropout

    if (self.weight_initialization == "randomize"):
      self.parameters["W"+str(self.total_layers)],self.parameters["b"+str(self.total_layers)] = weight_initializer.weight_initialize_randomize(hidden_units,self.layer_dims[-1],self.random_initializer)
    
    elif (self.weight_initialization == "xavier"):
      self.parameters["W"+str(self.total_layers)],self.parameters["b"+str(self.total_layers)] = weight_initializer.weight_initialize_xavier(hidden_units,self.layer_dims[-1])

    elif (self.weight_initialization == "he"):
      self.parameters["W"+str(self.total_layers)],self.parameters["b"+str(self.total_layers)] = weight_initializer.weight_initialize_he(hidden_units,self.layer_dims[-1])

    self.activations["AF"+str(self.total_layers)] = activation_function
    self.layer_dims.append(hidden_units)
    self.total_layers += 1




  def compile(self,cost_function = "crossEntropy", optimizer = 'gradient', learning_rate = 0.01, momentum_beta = 0.9, rms_beta = 0.999, adam_beta1=0.9, adam_beta2=0.999,batch_normalization = False):

    optimizers = Optimizers()

    self.cost_function = cost_function
    self.optimizer = optimizer
    self.learning_rate = learning_rate
    self.momentum_beta = momentum_beta
    self.rms_beta = rms_beta
    self.adam_beta1 = adam_beta1
    self.adam_beta2 = adam_beta2

    if optimizer == "momentum":
      self.momentum_parameters = optimizers.initialize_momentum(self.parameters,self.total_layers)

    elif optimizer == "rmsProp":
      self.rms_parameters = optimizers.initialize_rmsProp(self.parameters,self.total_layers)

    elif optimizer == "adam":
      self.momentum_parameters,self.rms_parameters = optimizers.initialize_adam(self.parameters,self.total_layers)
    



  def train(self,X,Y,number_of_epoch = 1000,batch_size=0,print_every = 100):
    #np.random.seed(1)
    if self.normalization == True:
      self.input_mean = np.mean(X,axis=1,keepdims = True)
      self.input_variance = np.var(X,axis=1, keepdims = True)
      X = np.divide(X-self.input_mean,np.sqrt(self.input_variance)+epsilon)
    
    self.batch_size = batch_size

    if (self.batch_size == 0):
      self.mini_batches.append((X,Y))
      self.mini_iterations = 1

    else:
      self.mini_batches,self.mini_iterations = generate_mini_batches(X, Y, self.batch_size)

    for i in range(number_of_epoch):

      if (self.mini_iterations != 1):
        self.mini_batches,self.mini_iterations = generate_mini_batches(X, Y, self.batch_size)

      for minibatch in self.mini_batches:

        (minibatch_X,minibatch_Y) = minibatch

        self.cache = forward_propagation(minibatch_X,self.total_layers,self.parameters,self.activations,self.dropout_layers)

        Y_pred = self.cache["A"+str(self.total_layers-1)]
        self.cost = compute_cost(Y_pred,minibatch_Y,self.cost_function,self.parameters,self.regularizer_layers)

        self.grads = backward_propagation(minibatch_Y,self.cost_function,self.parameters,self.cache,self.activations,self.total_layers-1,self.regularizer_layers,self.dropout_layers)

        self.adam_t += 1
        self.parameters = update_parameters(self.parameters,self.momentum_parameters,self.rms_parameters,self.adam_t,self.grads,self.learning_rate,self.total_layers,self.optimizer,self.momentum_beta,self.rms_beta,self.adam_beta1,self.adam_beta2)

      if i % print_every == 0:
        print ("Cost after iteration %i: %f" % (i,self.cost))
        self.cost_graph.append(self.cost)
    
    plt.figure(figsize=(10,6))
    plt.plot(np.squeeze(self.cost_graph))
    plt.ylabel('cost')
    plt.xlabel('iterations every'+str(print_every))
    plt.title("Learning rate =" + str(self.learning_rate))
    plt.show()