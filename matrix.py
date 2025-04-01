class Matrix:
	def __init__(self, rows=None, columns=None):
		self.determinant = None
		if columns != None:
			self.columns = columns
			self.rows = rows
			self.matrix = [[0 for column in range(self.columns)] for row in range(self.rows)]
		else:
			self.get_matrix()

	def get_matrix(self):
		while True:
			try:
				rows, columns = input('What size do you want your matrix? ').split('x')
				rows, columns = int(rows[0]), int(columns[0])
				self.rows, self.columns = rows, columns
				break
			except ValueError or UnboundLocalError or IndexError:
				print("""Please enter integers in the format AxB, where A is t
						he number of rows, and B is the number of columns.""")
		self.matrix = [[0 for column in range(columns)] for row in range(rows)]
		matrix = self.matrix
		for row in range(rows):
			while True:
				matrix[row] = input(f"Enter values for row {row+1}: ").split()
				if  len(matrix[row]) != len(range(columns)):
					print(f"There must be {columns} values in your row")
					continue
				i = 0
				for num in matrix[row]:
					try:
						num = float(num)
						if num.is_integer():
							num = int(num)
						matrix[row][i] = num
						i += 1   
					except ValueError:
						print("Please enter valid numbers")
						continue
				break
		return matrix

	def update(self):
		self.rows = len(self.matrix)
		self.columns = len(self.matrix[0])
		self.matrix = [[int(entry) if (not isinstance(entry, int)) and (entry.is_integer()) else entry for entry in row] for row in self.matrix]

	def duplicate(self):
		self.update()
		duplicate = Matrix(self.rows, self.columns)
		for i in range(self.rows):
			for j in range(self.columns):
				duplicate.matrix[i][j] = self.matrix[i][j]
		return duplicate

	def edit(self):
		while True:
			row = int(input('Which row do you want to edit? ')) - 1
			if row in range(self.rows):
				break
			print("The matrix does not have that many rows.")
		while True:
			column = int(input("Which column do you want to edit? ")) - 1
			if column in range(self.columns):
				break
			print("The matrix does not have that many columns.")
		while True:
			number = input("What do you want to change this cell to? ")
			if number.isdigit():
				number = float(number)
				break
			print("Please enter a number.")
		if number.is_integer():
			number = int(number)
		self.matrix[row][column] = number
		self.determinant = None

	def __add__(self, other):
		if isinstance(other, Matrix) and other.rows == self.rows and other.columns == self.columns:
			result = Matrix(self.rows, self.columns)
			for row in range(self.rows):
				for column in range(self.columns):
					result.matrix[row][column] = self.matrix[row][column] + other.matrix[row][column]
			result.update()
			return result
		
	def __mul__(self, other):
		if (not isinstance(other, Matrix)) and (isinstance(other, (int, float))):
			result = Matrix(self.rows, self.columns)
			for row in range(self.rows):
				for num in range(self.columns):
					result.matrix[row][num] = self.matrix[row][num]*other
		elif self.columns == other.rows:
			result = Matrix(self.rows, other.columns)
			for i in range(self.rows):
				for j in range(other.columns):
					for k in range(other.rows):
						result.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
		result.update()
		return result
		
	def transpose(self):
		result = Matrix(self.columns, self.rows)
		result.matrix = [[self.matrix[j][i]for j in range(result.columns)] for i in range(result.rows)]
		return result

	def get_determinant(self):
		if not self.determinant:
			result = self.duplicate() # initialize result matrix
			swaps = 0 # set swap counter
			# loop through each row starting from the top (forward elimination)
			for i in range(result.rows):
				# swap current row with a row below until pivot is not 0
				if result.matrix[i][i] == 0:
					for j in range(i+1, result.rows):
						if result.matrix[j][i] != 0:
							result.matrix[i], result.matrix[j] = result.matrix[j], result.matrix[i]
							swaps += 1
							break
						elif j == result.rows - 1:
							self.determinant = 0
							return 0
				# eliminate entries below pivot of current row
				for row in range(i+1, result.rows):
					if result.matrix[row][i] != 0:
						result.matrix[row] = [(result.matrix[row][j] - result.matrix[row][i]/result.matrix[i][i]*result.matrix[i][j]) for j in range(result.columns)]
			product = (-1)**swaps
			for i in range(result.rows): product *= result.matrix[i][i]
			self.determinant = product
		return self.determinant

	def rref(self):
		# initialize result matrix
		result = self.duplicate()
		# set leading column number (acts as i + # of skipped columns)
		lead = 0
		flag = False # set flag to break out of while loop
		# loop through each row starting from the top (forward elimination)
		for i in range(result.rows):
			# break if the leading column is >= # of columns
			if lead >= result.columns:
				break
			# swap current row with a row below until pivot is not 0
			while True:
				if result.matrix[i][lead] == 0:
					for j in range(i+1, result.rows):
						if result.matrix[j][lead] != 0:
							result.matrix[i], result.matrix[j] = result.matrix[j], result.matrix[i]
							flag = True
							break
						elif j == result.rows - 1:
							lead += 1
					if flag: break
				else:
					break
			# multiply current row by a scalar to make the pivot entry 1
			if result.matrix[i][lead] != 1:
				result.matrix[i] = [j/result.matrix[i][lead] for j in result.matrix[i]]
			# eliminate entries below pivot of current row
			for row in range(i+1, result.rows):
				if result.matrix[row][lead] != 0:
					result.matrix[row] = [(result.matrix[row][j] - result.matrix[row][lead]*result.matrix[i][j]) for j in range(result.columns)]
			lead += 1
		# loop through matrix starting at the bottom to eliminate elements above diagonal (backward elimination)
		for i in range(result.rows-1, -1, -1):
			pivot = None
			for column in range(result.columns):
				if abs(result.matrix[i][column] - 1) < 1e-9:
					pivot = column
			if pivot != None:
				for row in range(i-1, -1, -1):
					result.matrix[row] = [(result.matrix[row][j] - result.matrix[row][pivot]*result.matrix[i][j]) for j in range(result.columns)]
		# return result matrix
		return result
		
	def invert(self):
		# Augment matrix with identity matrix
		aug_matrix = Matrix(self.rows, self.columns*2)
		for i in range(self.rows):
			for j in range(self.columns):
				aug_matrix.matrix[i][j] = self.matrix[i][j]
			aug_matrix.matrix[i][i+self.columns] = 1
		aug_matrix = aug_matrix.rref()
		# return right half of augmented matrix if self.matrix is not singular
		# in singular matrices in rref, last row is all zeros
		if any(aug_matrix.matrix[-1][:self.columns]):
			result = Matrix(self.rows, self.columns)
			result.matrix = [row[self.columns:] for row in aug_matrix.matrix]
			return result
		else:
			raise ValueError('Singular matrices cannot be inverted')
		

	def __pow__(self, power):
		if self.rows == self.columns and isinstance(power, int):
			if power < 0:
				return self.invert()**-power
			elif power == 0:
				result = Matrix(self.rows, self.columns)
				for i in range(self.columns):
					result.matrix[i][i] = 1
				return result
			else:
				result = self.duplicate()
				for i in range(power-1):
					result *= self
				return result

	def trace(self):
		if self.rows == self.columns:
			result = 0
			for i in range(self.rows):
				result += self.matrix[i][i]
			return result

	def __sub__(self, other):
		return self + other*-1

	def __truediv__(self, other):
		if isinstance(other, (int, float)) and other != 0:
			return self*(1/other)