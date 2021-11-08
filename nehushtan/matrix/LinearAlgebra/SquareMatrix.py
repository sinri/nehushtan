from nehushtan.matrix.LinearAlgebra.Matrix import Matrix


class SquareMatrix(Matrix):
    def __init__(self, two_dimision_data=None):
        super().__init__(two_dimision_data)
        if not self.is_square_matrix():
            raise RuntimeError('Data is not for a Square Matrix')

    @staticmethod
    def make_identity_matrix(n: int):
        """
        n阶单位矩阵
        是一个n*n的方形矩阵，其主对角线元素为1，其余元素为0。单位矩阵以I[n]表示
        """
        x = []
        for i in range(n):
            y = []
            for j in range(n):
                if i == j:
                    y.append(1)
                else:
                    y.append(0)
            x.append(y)
        return SquareMatrix(x)

    def is_invertible_with_another_square_matrix(self, another_square_matrix: "SquareMatrix"):
        if not another_square_matrix.is_square_matrix():
            raise RuntimeError('Param another_square_matrix is not a Square Matrix')
        maybe_i_matrix = self.do_operation_matrix_multiplication(another_square_matrix)
        cell00 = maybe_i_matrix.get_cell(0, 0)
        if cell00 == 0:
            return False
        result_matrix = maybe_i_matrix.do_operation_scalar_multiplication(1.0 / cell00)
        for i in result_matrix.get_total_rows():
            for j in result_matrix.get_total_columns():
                cell = result_matrix.get_cell(i, j)
                if i == j and cell != 1:
                    return False
                if i != j and cell != 0:
                    return False
        return True

    def get_trace(self):
        """
        在线性代数中，一个n*n的矩阵A的迹（或迹数），
        是指A的主对角线（从左上方至右下方的对角线）上各个元素的总和，一般记作tr(A)或Sp(A)
        """
        trace = 0
        for i in self.get_total_rows():
            trace += self.get_cell(i, i)
        return trace
