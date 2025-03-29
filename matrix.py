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
		for i in range(self.rows):
			for j in range(self.columns):
				if not isinstance(self.matrix[i][j], int):
					if self.matrix[i][j].is_integer():
						self.matrix[i][j] = int(self.matrix[i][j])

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
		for i in range(self.rows):
			for j in range(self.columns):
				result.matrix[j][i] = self.matrix[i][j]
		return result

	def get_cofactor(self, row, column):
		copy = self.duplicate()
		for i in range(copy.rows):
			copy.matrix[i].pop(column)
		copy.matrix.pop(row)
		sign = (-1)**(row+column)
		cofactor = sign * copy.get_determinant()
		del copy
		return cofactor

	def get_determinant(self):
		matrix = self.matrix
		self.update()
		if not self.determinant:
			if self.columns == self.rows == 1:
				self.determinant = self.matrix[0][0]
			elif self.columns == self.rows == 2:
				determinant = (matrix[0][0]*matrix[1][1]) - (matrix[1][0]*matrix[0][1])
				self.determinant = determinant
			elif self.columns == self.rows:
				total = 0
				for i in range(self.columns):
					a = matrix[0][i]
					total += a * self.get_cofactor(0, i)
				self.determinant = total
		return self.determinant
	
	def inverse(self):
		# Augment matrix with identity matrix
		aug_matrix = Matrix(self.rows, self.columns*2)
		for i in range(self.rows):
			for j in range(self.columns):
				aug_matrix.matrix[i][j] = self.matrix[i][j]
			aug_matrix.matrix[i][i+self.columns] = 1
		# loop through each row starting from the top (forward elimination)
		for i in range(aug_matrix.rows):
			# swap current row with a row below until pivot is not 0
			if aug_matrix.matrix[i][i] == 0:
				for j in range(i+1, aug_matrix.rows):
					if aug_matrix[j][i] != 0:
						aug_matrix.matrix[i], aug_matrix.matrix[j] = aug_matrix.matrix[j], aug_matrix.matrix[i]
					elif j == aug_matrix.rows - 1:
						raise ValueError('Singular matrices do not have an inverse.')
			# multiply current row by a scalar to make the pivot entry 1
			if aug_matrix.matrix[i][i] != 1:
				scalar = 1/aug_matrix.matrix[i][i]
				for k in range(aug_matrix.columns):
					aug_matrix.matrix[i][k] *= scalar
			# eliminate entries below pivot of current row
			for row in range(i+1, aug_matrix.rows):
				if aug_matrix.matrix[row][i] != 0:
					aug_matrix.matrix[row] = [(aug_matrix.matrix[i][j] + aug_matrix.matrix[row][j]*(-1/aug_matrix.matrix[row][i])) for j in range(aug_matrix.columns)]
		# loop through matrix starting at the bottom to eliminate elements above diagonal (backward elimination)
		for i in range(aug_matrix.rows-1, -1, -1):
			for row in range(i-1, -1, -1):
				scaled_pivot = [j*aug_matrix.matrix[row][i] for j in aug_matrix.matrix[i]]
				aug_matrix.matrix[row] = [(aug_matrix.matrix[row][j] - scaled_pivot[j]) for j in range(aug_matrix.columns)]
		#return inverse
		result = Matrix(self.rows, self.columns)
		result.matrix = [row[self.columns:] for row in aug_matrix.matrix]
		return result
						

	def _multiply_row(self, row, scalar):
		for i in range(self.columns):
			self.matrix[row][i] *= scalar

	def get_adjoint(self):
		cofactor_matrix = Matrix(self.rows, self.columns)
		for i in range(self.rows):
			for j in range(self.columns):
				cofactor_matrix.matrix[i][j] = self.get_cofactor(i, j)
		adjoint_matrix = cofactor_matrix.transpose()
		return adjoint_matrix
		
	def invert(self):
		if self.rows == self.columns:
			determinant = self.get_determinant()
			if determinant != 0:
				inverse = self.get_adjoint()*(1/determinant)
				inverse.update()
				return inverse

	def __pow__(self, power):
		if self.rows == self.columns and isinstance(power, int):
			if power < 0:
				return self.inverse()**-power
			elif power == 0:
				result = Matrix(self.rows, self.columns)
				for i in range(self.columns):
					result.matrix[i][i] = 1
				return result
			else:
				result = self.duplicate()
				for i in range(power-1):
					result = self*result
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

# B = Matrix(9, 9)
# B.matrix = [
# 	[2, 1, 4, -1, 3, 0, 5, -2, 1], 
# 	[-1, 3, -2, 2, 1, -4, 0, 1, 3], 
# 	[0, -2, 1, 3, -5, 1, 2, 0, -1], 
# 	[3, 0, -5, -2, 4, 2, -1, 3, 0], 
# 	[1, -4, 3, 0, -1, 5, 3, -2, 2], 
# 	[-2, 1, 0, 5, 2, -3, 4, 1, -4], 
# 	[5, 2, -1, -3, 0, 4, -2, 0, 3], 
# 	[-3, 4, 2, 1, -2, 0, 1, 5, -1], 
# 	[4, -1, -3, -4, 3, 1, 0, -2, 5]]

B = Matrix(4, 4)
B.matrix = [
	[1, 2, 0, 1],
	[0, 1, 3, -1],
	[-1, 0, 1, 4],
	[2, -1, -2, 0]
]

# B = Matrix(3, 3)
# B.matrix = [[1, 2, 1],
# 			[2, 3, 3],
# 			[2, 8, 4]]
import time
a_time = time.time()
print(B.inverse().matrix)
a_time = time.time()-a_time

b_time = time.time()
print(B.invert().matrix)
b_time = time.time()-b_time

print(a_time)
print(b_time)
