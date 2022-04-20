import random

class Matrix():
	"""docstring for Matrix"""
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.data = []

		for i in range(self.rows):
			self.data.append([])
			for j in range(self.cols):
				self.data[i].append(0)


	def copy(self):
		m = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				m.data[i][j] = self.data[i][j]
		return m

	@staticmethod
	def array_to_matrix(a):
		"""					[
							[a],
							[b],
		[a, b, c, d, e] ->	[c],
		 					[d],
							[e]
							]
		"""

		m = Matrix(len(a), 1)
		for i in range(len(a)):
			m.data[i][0] = a[i]
		return m

	@staticmethod
	def matrix_to_array(m):mat
		a = []
		for i in range(m.rows):
	   		for j in range(m.cols):
	   			a.append(m.data[i][j])
		return a


	def transpose(self):
		"""
			A B C    A D H
			D F G -> B F I
			H I J    C G J
		"""
		result = Matrix(self.cols, self.rows)
		for i in range(self.rows):
			for j in range(self.cols):
				result.data[j][i] = self.data[i][j]
		self.data = result.data

	def table(self):
		for i in range(self.rows):
			print(self.data[i])

	def randomize(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.data[i][j] = round(random.random() * 2 - 1, 3)

	def add(self, n):
		if isinstance(n, Matrix):
			for i in range(self.rows):
				for j in range(self.cols):
					self.data[i][j] += n.data[i][j]
		else:
			for i in range(self.rows):
				for j in range(self.cols):
					self.data[i][j] += n

	@staticmethod
	def subtract(m1, m2):
		m = Matrix(m1.rows, m1.rows)
		for i in range(m1):
			for j in range(m2):
				m.data[i][j] = m1.data[i][j] - m2.data[i][j]
		return m

	@staticmethod
	def multiply_2(a, b):
	    """Matrix Product"""
	    if a.cols != b.rows:
	    	print('Columns of A must match rows of B.')
	    	return "Undefined"

	    result = Matrix(a.rows, b.cols)
	    for i in range(result.rows):
	      for j in range(result.cols):
	        sum = 0
	        for k in range(a.cols):
	          sum += a.data[i][k] * b.data[k][j]

	        result.data[i][j] = sum
	    return result

	def multiply(self, n):
		"""Hadamard product if n is another Matrix, else Scalar product."""
		if isinstance(n, Matrix):
			for i in range(self.rows):
				for j in range(self.cols):
					self.data[i][j] *= n.data[i][j]
		else:
			for i in range(self.rows):
				for j in range(self.cols):
					self.data[i][j] *= n

	def map(self, f):
		"""Applies a function to every element of the matrix"""
		for i in range(self.rows):
			for j in range(self.cols):
				val = self.data[i][j]
				self.data[i][j] = f(val)
