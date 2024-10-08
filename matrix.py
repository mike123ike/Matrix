class Matrix:
    def __init__(self, rows=None, columns=None):
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

    def add(self, other):
        if isinstance(other, Matrix) and other.rows == self.rows and other.columns == self.columns:
            result = Matrix(self.rows, self.columns)
            for row in self.matrix:
                for column in range(self.columns):
                    result.matrix[row][column] = self.matrix[row][column] + other.matrix[row][column]
            result.update
            return result
        
    def multiply(self, other):
        if not isinstance(other, Matrix):
            result = Matrix(self.rows, self.columns)
            for row in range(self.rows):
                for num in range(self.columns):
                    result.matrix[row][num] = self.matrix[row][num]*other
            return result
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
        if self.columns == self.rows == 1:
            return self.matrix[0][0]
        elif self.columns == self.rows == 2:
            determinant = (matrix[0][0]*matrix[1][1]) - (matrix[1][0]*matrix[0][1])
            return determinant
        elif self.columns == self.rows:
            total = 0
            for i in range(self.columns):
                a = matrix[0][i]
                total += a * self.get_cofactor(0, i)
            return total
        
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
                inverse = self.get_adjoint().multiply(1/determinant)
                inverse.update()
                return inverse
    
    def exponent(self, power):
        if self.rows == self.columns:
            result = self.duplicate()
            for i in range(power-1):
                result = self.multiply(result)
            return result