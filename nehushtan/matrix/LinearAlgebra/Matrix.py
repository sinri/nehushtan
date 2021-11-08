import copy
from typing import List

from nehushtan.matrix.LinearAlgebra.Vector import Vector


class Matrix:
    def __init__(self, two_dimision_data=None):
        self.__data: List[List[float]] = []

        if two_dimision_data is not None:
            if type(two_dimision_data) is not tuple and type(two_dimision_data) is not list:
                raise RuntimeError('two_dimision_data invalid')
            length_set = set()
            for one_dimision_data in two_dimision_data:
                if type(one_dimision_data) is not tuple and type(one_dimision_data) is not list:
                    raise RuntimeError('one_dimision_data in two_dimision_data invalid')
                length_set.add(len(one_dimision_data))
            if len(length_set) > 1:
                raise RuntimeError('Length of each one_dimision_data in two_dimision_data not same')
            self.__data = two_dimision_data

    def is_square_matrix(self):
        return self.get_total_rows() == self.get_total_columns()

    def _get_raw_data(self):
        return self.__data

    def get_cell(self, row: int, column: int):
        return self.__data[row][column]

    def get_total_rows(self):
        return len(self.__data)

    def get_total_columns(self):
        if self.get_total_rows() == 0:
            return 0
        return len(self.__data[0])

    def is_square_matrix(self):
        return self.get_total_rows() == self.get_total_columns()

    def get_row_vector(self, row: int):
        return Vector(Vector.VECTOR_TYPE_ROW, self.__data[row])

    def get_column_vector(self, column: int):
        x = []
        for datum in self.__data:
            x.append(datum[column])
        return Vector(Vector.VECTOR_TYPE_COLUMN, x)

    def do_operation_addition(self, another_matrix: "Matrix"):
        if self.get_total_rows() != another_matrix.get_total_rows() \
                or self.get_total_columns() != another_matrix.get_total_columns():
            raise RuntimeError('Two matrixes are not in save size')

        result_data = []
        for row in range(self.get_total_rows()):
            result_row = []
            for column in range(self.get_total_columns()):
                result_row.append(self.get_cell(row, column) + another_matrix.get_cell(row, column))
            result_data.append(result_row)

        return Matrix(result_data)

    def do_operation_scalar_multiplication(self, scalar):
        result_data = []
        for row in range(self.get_total_rows()):
            result_row = []
            for column in range(self.get_total_columns()):
                result_row.append(self.get_cell(row, column) * scalar)
            result_data.append(result_row)

        return Matrix(result_data)

    def do_operation_transposition(self):
        result_data = []
        # DEFAULT: EMPTY -> EMPTY
        if self.get_total_rows() > 0:
            # R * C -> C * R
            for column in range(self.get_total_columns()):
                result_row = []
                for row in range(self.get_total_rows()):
                    result_row.append(self.get_cell(row, column))
                result_data.append(result_row)

        return Matrix(result_data)

    def do_operation_matrix_multiplication(self, another_matrix: "Matrix"):
        if self.get_total_columns() != another_matrix.get_total_rows():
            raise RuntimeError(
                'Multiplication of two matrices is defined '
                'if and only if the number of columns of the left matrix '
                'is the same as the number of rows of the right matrix.'
            )
        result_data = []
        for row in range(self.get_total_rows()):
            result_row = []
            row_vector = self.get_row_vector(row)
            for column in range(another_matrix.get_total_columns()):
                column_vector = another_matrix.get_column_vector(column)
                # compute for the result cell
                computed_result_cell = Vector.multiplication_row_and_column_vector_pair(row_vector, column_vector)
                result_row.append(computed_result_cell)
            result_data.append(result_row)
        return Matrix(result_data)

    def do_row_addition(self, base_row: int, another_row: int, multiple: float = 1.0):
        base_row_vector = self.get_row_vector(base_row)
        another_row_vector = self.get_row_vector(another_row)
        result_row_vector = base_row_vector.do_operation_addition(another_row_vector, multiple)

        x = copy.deepcopy(self.__data)
        x[base_row] = result_row_vector.get_raw_vector_data()
        return Matrix(x)

    def do_row_multiplication_with_scalar(self, row: int, scalar: float):
        """
        row multiplication, that is multiplying all entries of a row by a non-zero constant;
        """
        if scalar == 0:
            raise RuntimeError('do_row_multiplication_with_zero is not supported')
        original_row_vector = self.get_row_vector(row)
        result_row_vector = original_row_vector.do_operation_scalar_multiplication(scalar)
        x = copy.deepcopy(self.__data)
        x[row] = result_row_vector.get_raw_vector_data()
        return Matrix(x)

    def do_row_switch(self, one_row: int, another_row: int):
        """
        row switching, that is interchanging two rows of a matrix;
        """
        x = copy.deepcopy(self.__data)
        t1 = copy.deepcopy(x[one_row])
        x[one_row] = copy.deepcopy(x[another_row])
        x[another_row] = t1
        return Matrix(x)

    def __str__(self):
        s = ''
        for datum in self.__data:
            s += f'{datum}\n'
        return s
