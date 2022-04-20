from libs.Matrix import *
import math
import pygame

def sigmoid(x):
	return round(1 / (1 + math.exp(-x)), 3)


def tanh(x):
	return math.tanh(x)




class NeuralNetwork():
	"""docstring for NeuralNetwork"""
	def __init__(self, inputNodes, hiddenNodes=1, outputNodes=1):
		if isinstance(inputNodes, NeuralNetwork):
			a = inputNodes
			self.inputNodes = a.inputNodes
			self.hiddenNodes = a.hiddenNodes
			self.outputNodes = a.outputNodes

			self.weights_input_hidden = a.weights_input_hidden.copy()
			self.weights_hidden_output = a.weights_hidden_output.copy()

			self.bias_hidden = a.bias_hidden.copy()
			self.bias_output = a.bias_output.copy()
			self.hidden = Matrix(0, 0)
		else:
			self.inputNodes = inputNodes
			self.hiddenNodes = hiddenNodes
			self.outputNodes = outputNodes

			self.weights_input_hidden = Matrix(self.hiddenNodes, self.inputNodes)
			self.weights_hidden_output = Matrix(self.outputNodes, self.hiddenNodes)
			self.weights_input_hidden.randomize()
			self.weights_hidden_output.randomize()

			self.bias_hidden = Matrix(self.hiddenNodes, 1)
			self.bias_output = Matrix(self.outputNodes, 1)
			self.bias_hidden.randomize()
			self.bias_output.randomize()
			self.hidden = Matrix(0, 0)



	def predict(self, input_array):
		"Feed forward"
		inputs = Matrix.array_to_matrix(input_array)

		self.hidden = Matrix.multiply_2(self.weights_input_hidden, inputs)

		self.hidden.add(self.bias_hidden)
		self.hidden.map(sigmoid)

		output = Matrix.multiply_2(self.weights_hidden_output, self.hidden)

		output.add(self.bias_output)
		output.map(tanh)

		output = Matrix.matrix_to_array(output)
		return output


	def predict_2(self, input_array):
			inputs = Matrix.array_to_matrix(input_array)
			print("INPUT LAYER")
			print("--------------------------------")
			inputs.table()
			print("--------------------------------")

			print("WEIGHTS_INPUT_HIDDEN X INPUT LAYER")
			print("--------------------------------")
			self.weights_input_hidden.table()
			print("---------------------------------")
			print("X")
			print("---------------------------------")
			inputs.table()
			self.hidden = Matrix.multiply_2(self.weights_input_hidden, inputs)
			print("--------------------------------")
			print("=")
			print("---------------------------------")
			print("HIDDEN LAYER")
			print("--------------------------------")
			self.hidden.table()
			print("--------------------------------")
			print("ADD BIAS")
			print("--------------------------------")
			self.hidden.table()
			print("+")
			self.bias_hidden.table()
			self.hidden.add(self.bias_hidden)
			print("=")
			self.hidden.table()
			print("--------------------------------")
			self.hidden.map(sigmoid)
			print("SIGMOID HIDDEN LAYER")
			print("--------------------------------")
			self.hidden.table()
			print("--------------------------------")
			print("WEIGHTS_HIDDEN_OUTPUT X HIDDEN LAYER")
			print("--------------------------------")
			self.weights_hidden_output.table()
			print("---------------------------------")
			print("X")
			print("---------------------------------")
			self.hidden.table()

			output = Matrix.multiply_2(self.weights_hidden_output, self.hidden)
			print("--------------------------------")
			print("=")
			print("---------------------------------")
			print("OUTPUT LAYER")
			print("--------------------------------")
			output.table()
			print("--------------------------------")

			print("ADD BIAS")
			print("--------------------------------")
			output.table()
			print("+")
			self.bias_output.table()
			output.add(self.bias_output)
			print("=")
			output.table()
			print("--------------------------------")
			output.map(tanh)
			print("TANH OUTPUT LAYER")
			print("--------------------------------")
			output.table()
			print("--------------------------------")

			output = Matrix.matrix_to_array(output)
			return output

	def train(input_array, desired_output):
		"Backpropogation"

		"Calculate the cost(error)"
		"go back through the network calculating the difference between the target and the output value for all output and hidden neurons"
		"weight output difference multiplied by the input activation to find the gradient"
		"subtract the learning rate from the weights gradient"
		"bigger learnign rate = more speed"
		"smaller learning rate = more accurate training"
		""

		"""
		Calculate the error
	    ERROR = TARGETS - OUTPUTS
	  	let gradient = outputs * (1 - outputs)
	    Calculate gradient
		Calculate deltas
		Adjust the weights by deltas
		Adjust the bias by its deltas (which is just the gradients)
		Calculate the hidden layer errors
	    Calculate hidden gradient
    	Calcuate input->hidden deltas
    	"""

		outputs = self.predict(input_array)

		targets = Matrix.array_to_matrix(desired_output)

		outputErrors = Matrix.subtract(targets, outputs)

	def copy(self):
		return NeuralNetwork(self)


	def mutate(self, f):
	    self.weights_input_hidden.map(f)
	    self.weights_hidden_output.map(f)
	    self.bias_hidden.map(f)
	    self.bias_output.map(f)
