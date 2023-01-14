import random
import numpy as np
import json


class NetworkNode:
    
    #Neural Network Layer Node
    def __init__(self):
        # Initialize the node with random weights
        self.weights = []
        self.value = 0
        self.delta = 0    
        
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
        
        outIdx = len(self.layers) - 1
        self.outputLayer = self.layers[outIdx]
        
    
    
    def setInputs(self,inputs):
        # Set the input layer values to the given inputs.
        for i in range(len(inputs)):
            self.inputLayer[i].value = inputs[i]
    
    
    def forwardPass(self):
        # Forward pass
        for layerID,layerNodeList in self.layers.items():
            if layerID == 0:
                continue
            # Node index in the layer.
            for idx in range(len(layerNodeList)):
                nodeSum = 0
                for i in range(len(self.layers[layerID - 1])):
                    nodeSum += self.layers[layerID - 1][i].weights[idx] * self.layers[layerID - 1][i].value

                layerNodeList[idx].value = sig(nodeSum)
        return
    
    
    def backwardPass(self,y):
        # Backward pass using deltas.
        for idx,node in enumerate(self.outputLayer):
            node.delta = dsig(node.value) * (y[idx] - node.value)
        

        for layerID,layerNodeList in reversed(self.layers.items()):
            if layerID == len(self.layers) - 1:
                continue

            for node in layerNodeList:
                sum = 0
                for i in range(len(self.layers[layerID+1])):
                    sum += (self.layers[layerID+1][i].delta * node.weights[i])
                node.delta = dsig(node.value) * sum
        return
    
    def updateWeights(self,learningRate):

        for layerID,layerNodeList in self.layers.items():            
            for node in layerNodeList:
                for i in range(len(node.weights)):
                    node.weights[i] += learningRate * node.delta * node.value
        return


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
        
def dsig(x):
    # Derrivative of sigmoid activation function.
    return np.exp(-x) / ((1+np.exp(-x))**2)
    

def mse(y, y_prime):
    return np.mean((y - y_prime)**2)


def BackPropagationLearner(X,y, net, learning_rate, epochs):    
    for epoch in range(epochs):
		# Iterate over each example in the dataset X,y.
        for data in X:
			# Activate input layer
            net.setInputs(data)
            
			# Forward pass
            net.forwardPass()
            
            # Error for the MSE cost function
            

            # Propagate deltas backward from output layer to input layer.
            net.backwardPass(y)


			#  Update weights
            net.updateWeights(learning_rate)


    # return the trained network
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
    


    layers = [len(X[0])]

    if hidden_layer_sizes is None:
        layers.append(3)
    else:
        layers += hidden_layer_sizes
        
    layers.append(np.unique(y).shape[0])


    firstNet = Network(layers)
    lastNet = BackPropagationLearner(X,y, firstNet, learning_rate, epochs)


    def predict(example):
        # set input layer values to example values
        lastNet.setInputs(example)
    
        # forward pass
        lastNet.forwardPass()
        
        # find the max node from output nodes 
        prediction = lastNet.outputLayer.index(max(lastNet.outputLayer, key=lambda x: x.value))
        return prediction

    return predict
	
from sklearn import datasets

random.seed(462)

iris = datasets.load_iris()
X = iris.data  
y = iris.target

nNL = NeuralNetLearner(X,y,hidden_layer_sizes=[3])
print(nNL([4.6, 3.1, 1.5, 0.2])) #0
print(nNL([6.5, 3. , 5.2, 2. ])) #2
