class Matrix:
	def __init__(self, rows=0, columns=0, data=None):
		self.determinant = None
		if data:
			# check if data is a list/tuple of lists/tuples
			# all sub-sequences are the same length
			# all entries inside the sub-sequences are ints or floats
			if isinstance(data, (list, tuple)) and all([
				isinstance(row, (list, tuple)) and
				len(row) == len(data[0]) and
				all([isinstance(entry, (int, float)) for entry in row]) 
				for row in data]):
				self.rows = len(data)
				self.columns = len(data[0])
				self.matrix = data
		else:
			self.columns = columns
			self.rows = rows
			self.matrix = [[0 for column in range(self.columns)] for row in range(self.rows)]
		
	def update(self):
		self.rows = len(self.matrix)
		self.columns = len(self[0])
		self.matrix = [[int(entry) if (not isinstance(entry, int)) and (entry.is_integer()) else entry for entry in row] for row in self.matrix]

	def duplicate(self):
		self.update()
		duplicate = Matrix(self.rows, self.columns)
		duplicate.matrix = [row[:] for row in self.matrix]
		duplicate.determinant = self.determinant
		return duplicate

	def __add__(self, other):
		if isinstance(other, Matrix) and other.rows == self.rows and other.columns == self.columns:
			result = Matrix(self.rows, self.columns)
			for row in range(self.rows):
				for column in range(self.columns):
					result[row][column] = self[row][column] + other[row][column]
			result.update()
			return result
		else:
			raise ValueError('Matrices can only be added to matrices with the same dimensions')
		
	def __mul__(self, other):
		if isinstance(other, (int, float)):
			result = self.duplicate()
			result.matrix = [[entry*other for entry in row] for row in result.matrix]
		elif isinstance(other, Matrix) and self.columns == other.rows:
			result = Matrix(self.rows, other.columns)
			result.matrix = [[sum(self[i][k] * other[k][j] for k in range(other.rows)) for j in range(other.columns)] for i in range(self.rows)]
		else:
			raise ValueError('Incompatible operands')
		result.update()
		return result
		
	def transpose(self):
		result = Matrix(self.columns, self.rows)
		result.matrix = [[self[j][i]for j in range(result.columns)] for i in range(result.rows)]
		return result

	def get_determinant(self):
		if not self.determinant:
			if self.rows == self.columns:
				result = self.duplicate() # initialize result matrix
				swaps = 0 # set swap counter
				# loop through each row starting from the top (forward elimination)
				for i in range(result.rows):
					# swap current row with a row below until pivot is not 0
					if result[i][i] == 0:
						for j in range(i+1, result.rows):
							if result[j][i] != 0:
								result[i], result[j] = result[j], result[i]
								swaps += 1
								break
							elif j == result.rows - 1:
								self.determinant = 0
								return 0
					# eliminate entries below pivot of current row
					for row in range(i+1, result.rows):
						if result[row][i] != 0:
							result[row] = [(result[row][j] - result[row][i]/result[i][i]*result[i][j]) for j in range(result.columns)]
				product = (-1)**swaps
				for i in range(result.rows): product *= result[i][i]
				self.determinant = product
			else:
				raise ValueError('Only square matrices have a determinant')
		return self.determinant

	def rref(self):
		# initialize result matrix
		result = self.duplicate()
		# set leading column number (acts as i + # of skipped columns)
		lead = 0
		# loop through each row starting from the top (forward elimination)
		for i in range(result.rows):
			if not any(result[i]):
				break
			# break if the leading column is >= # of columns
			if lead >= result.columns:
				break
			# find a suitable pivot row and swap with the current row
			pivot = i
			while lead < result.columns:
				if result[pivot][lead] == 0:
					pivot += 1
					if pivot == result.rows:
						pivot = i
						lead += 1
				else:
					break
			if pivot != i:
				result[i], result[pivot] = result[pivot], result[i]
			# multiply current row by a scalar to make the pivot entry 1
			if result[i][lead] != 1:
				result[i] = [j/result[i][lead] for j in result[i]]
			# eliminate entries below pivot of current row
			for row in range(i+1, result.rows):
				if result[row][lead] != 0:
					result[row] = [(result[row][j] - result[row][lead]*result[i][j]) for j in range(result.columns)]
			lead += 1
		# loop through matrix starting at the bottom to eliminate elements above diagonal (backward elimination)
		for i in range(result.rows-1, -1, -1):
			pivot = None
			for column in range(result.columns):
				if abs(result[i][column] - 1) < 1e-9:
					pivot = column
			if pivot != None:
				for row in range(i-1, -1, -1):
					result[row] = [(result[row][j] - result[row][pivot]*result[i][j]) for j in range(result.columns)]
		# return result matrix
		result.update()
		return result
		
	def invert(self):
		if self.rows == self.columns:
			# Augment matrix with identity matrix
			aug_matrix = Matrix(self.rows, self.columns*2)
			for i in range(self.rows):
				for j in range(self.columns):
					aug_matrix[i][j] = self[i][j]
				aug_matrix[i][i+self.columns] = 1
			aug_matrix = aug_matrix.rref()
			# return right half of augmented matrix if self.matrix is not singular
			# in singular matrices in rref, last row is all zeros
			if any(aug_matrix[-1][:self.columns]):
				result = Matrix(self.rows, self.columns)
				result.matrix = [row[self.columns:] for row in aug_matrix.matrix]
				return result
			else:
				raise ValueError('Singular matrices cannot be inverted')
		else:
			raise ValueError('Only square matrices can be inverted')
		
	def __pow__(self, power):
		if self.rows == self.columns and isinstance(power, int):
			if power < 0:
				return self.invert()**-power
			elif power == 0:
				result = Matrix(self.rows, self.columns)
				for i in range(self.columns):
					result[i][i] = 1
				return result
			else:
				result = self.duplicate()
				for i in range(power-1):
					result *= self
				return result
		elif self.rows != self.columns:
			raise ValueError('Only square matrices can be raised to a power')
		else:
			raise ValueError('Only integers can be used as a power')

	def trace(self):
		if self.rows == self.columns:
			result = 0
			for i in range(self.rows):
				result += self[i][i]
			return result
		else:
			raise ValueError('Only square matrices have a trace')

	def __sub__(self, other):
		return self + other*-1

	def __truediv__(self, other):
		if isinstance(other, (int, float)) and other != 0:
			return self*(1/other)
		else:
			raise ValueError('Matrices can only be divided by numbers')
	
	def __getitem__(self, key):
		return self.matrix[key]
	
	def __setitem__(self, key, value):
		self.matrix[key] = value