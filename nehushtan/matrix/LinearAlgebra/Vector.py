from typing import List


class Vector:
    VECTOR_TYPE_ROW = 'R'
    VECTOR_TYPE_COLUMN = 'C'

    def __init__(self, vecotr_type: str, vector_data=None):
        self.__vector_type = vecotr_type
        self.__vector_data: List[float] = []
        if type(vector_data) is not tuple and type(vector_data) is not list:
            raise RuntimeError('vector data should be list')
        self.__vector_data = vector_data

    def get_vector_type(self):
        return self.__vector_type

    def get_raw_vector_data(self):
        return self.__vector_data

    def get_size(self):
        return len(self.__vector_data)

    def get_element(self, index: int):
        return self.__vector_data[index]

    @staticmethod
    def multiplication_row_and_column_vector_pair(row_vector: "Vector", column_vector: "Vector"):
        if row_vector.get_size() != column_vector.get_size():
            raise RuntimeError('Two vectors hold not same size')
        x = 0.0
        for i in range(row_vector.get_size()):
            x += row_vector.get_element(i) * column_vector.get_element(i)
        return x

    def do_operation_scalar_multiplication(self, scalar: float):
        x = []
        for i in range(len(self.__vector_data)):
            x.append(self.__vector_data[i] * scalar)
        return Vector(self.__vector_type, x)

    def do_operation_addition(self, another_vector: "Vector", multiple: float = 1.0):
        if self.get_size() != another_vector.get_size():
            raise RuntimeError('Two vectors hold not same size')

        x = []
        for i in range(len(self.__vector_data)):
            x.append(self.get_element(i) + multiple * another_vector.get_element(i))
        return Vector(self.__vector_type, x)
