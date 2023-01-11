import random
import numpy as np
import json
class Network:
    #Create Directed Acyclic Network of given number layers.
    def __init__(self,layers):
        self.layers = layers
        self.weights = {}

        
        for layerIdx,currLayerSize in enumerate(layers):
            self.weights[layerIdx] = {}
            for nodeIdx in range(currLayerSize):
                self.weights[layerIdx][nodeIdx] = {}
                for nextLayerSize in layers[layerIdx+1:]:
                    for nextNodeIdx in range(nextLayerSize):
                        self.weights[layerIdx][nodeIdx][nextNodeIdx] = random.uniform(-0.5,0.5)
        
        print(self.weights)


        







        



def BackPropagationLearner(X,y, net, learning_rate, epochs):


	
    # initialize each weight with the values min_value=-0.5, max_value=0.5,


    for epoch in range(epochs):
		# Iterate over each example
        

        



	
			# Activate input layer
			
			# Forward pass
			
			# Error for the MSE cost function
			
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
    

    layers = [X.shape[1]] + [hidden_layer_sizes] + [np.unique(y).shape[0]]

    net = Network(layers)
    BackPropagationLearner(X,y, net, learning_rate, epochs)


    def predict(example):
        # activate input layer


        # set input layer values to example values


        # forward pass


        # find the max node from output nodes 
        return prediction

    return predict
	
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data  
y = iris.target

nNL = NeuralNetLearner(X,y, hidden_layer_sizes=3, learning_rate=0.01, epochs=100)
print(nNL([4.6, 3.1, 1.5, 0.2])) #0
print(nNL([6.5, 3. , 5.2, 2. ])) #2
