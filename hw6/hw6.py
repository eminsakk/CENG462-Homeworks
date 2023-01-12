import random
import numpy as np
import json


class NetworkNode:
    
    
    #Bayesian Network Layer Node
    def __init__(self):
        # Initialize the node with random weights
        self.weights = []
        self.value = 0
        self.delta = 0
        pass
    
    
    def __str__(self):
        return "     Weights: " + str(self.weights)
    
        

class Network:
    #Create Directed Acyclic Network of given number layers.

    def __init__(self,layers):
        # Inıtialize the network with given number of layers and nodes.
        
        self.layers = {}
        
        for i in range(len(layers)):
            self.layers[i] = []
            nodeNumber = layers[i]
            for j in range(nodeNumber):
                self.layers[i].append(NetworkNode())
            
        
        # Initialze the weights of the network nodes with the values min_value=-0.5, max_value=0.5.
        for i in range(len(self.layers) - 1):
            currLayerNodes = self.layers[i]
            nextLayerNodes = self.layers[i+1]
            
            for nNode in currLayerNodes:
                for nextLayerNode in nextLayerNodes:
                    nNode.weights.append(random.uniform(-0.5,0.5))
                

        self.inputLayer = self.layers[0]
        self.outputLayer = self.layers[len(self.layers) - 1]
        
    
    
    def setInputs(self,inputs):
        # Set the input layer values to the given inputs.
        for i in range(len(inputs)):
            self.inputLayer[i].value = inputs[i]
    
    def __str__(self):
        ret = ""
        
        for layer in self.layers:
            ret += "Layer: " + str(layer) + "\n"

            for node in self.layers[layer]:
                ret += str(node) + " "
            
        return ret
        
    
    
    
def sig(x):
    #Sigmoid activation function.
    return 1 / (1+np.exp(-x))    
        
        
    

def BackPropagationLearner(X,y, net, learning_rate, epochs):    
    # initialize each weight with the values min_value=-0.5, max_value=0.5,
    for epoch in range(epochs):
		# Iterate over each example in the dataset X,y.

        for data in X:
			# Activate input layer
            net.setInputs(data)
            
			# Forward pass
			
            for layer in net.layers:
                if layer == 0:
                    continue
                else:
                    for node in net.layers[layer]:
                        sum = 0
                        for i in range(len(net.layers[layer-1])):
                            sum += net.layers[layer-1][i].value * node.weights[i]
                        node.value = sig(sum)
            
    
			# Error for the MSE cost function
            for i in range(len(net.outputLayer)):
                net.outputLayer[i].delta = (net.outputLayer[i].value - y[i]) * net.outputLayer[i].value * (1 - net.outputLayer[i].value)

            for layer in reversed(net.layers):
                if layer == len(net.layers) - 1:
                    continue
                else:
                    for node in net.layers[layer]:
                        sum = 0
                        for i in range(len(net.layers[layer+1])):
                            sum += net.layers[layer+1][i].delta * node.weights[i]
                        node.delta = node.value * (1 - node.value) * sum
            
            for layer in net.layers:
                for node in net.layers[layer]:
                    for i in range(len(node.weights)):
                        node.weights[i] += learning_rate * net.layers[layer-1][i].value * node.delta
            
			# The activation function used is sigmoid function
			
			# Backward pass

			#  Update weights
        pass

		

    return net



def NeuralNetLearner(X,y, hidden_layer_sizes=None, learning_rate=0.01, epochs=100):
    """
    Layered feed-forward network.
    hidden_layer_sizes: List of number of hidden units per hidden layer if None set 3
    learning_rate: Learning rate of gradient descent
    epochs: Number of passes over the dataset
    activation:sigmoid 
	"""

    # construct a raw network and call BackPropagationLearner
    


    layers = [4,3,3]
    net = Network(layers)
    print(net)
    BackPropagationLearner(X,y, net, learning_rate, epochs)


    def predict(example):
        # activate input layer

        
        

        # set input layer values to example values
        net.setInputs(example)
        
        
        # forward pass
        for layer in net.layers:
            if layer == 0:
                continue
            else:
                for node in net.layers[layer]:
                    sum = 0
                    for i in range(len(net.layers[layer-1])):
                        sum += net.layers[layer-1][i].value * node.weights[i]
                    node.value = sig(sum)
                    
        # find the max node from output nodes 
        prediction = net.outputLayer.index(max(net.outputLayer, key=lambda x: x.value))
        return prediction

    return predict
	
from sklearn import datasets

random.seed(462)

iris = datasets.load_iris()
X = iris.data  
y = iris.target

nNL = NeuralNetLearner(X,y, hidden_layer_sizes=3, learning_rate=0.01, epochs=100)
print(nNL([4.6, 3.1, 1.5, 0.2])) #0
print(nNL([6.5, 3. , 5.2, 2. ])) #2
