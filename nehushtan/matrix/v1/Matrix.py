from typing import List, Dict

from nehushtan.matrix.v1.Column import Column
from nehushtan.matrix.v1.Condition import Condition
from nehushtan.matrix.v1.Row import Row


class Matrix:
    def __init__(self, data):
        self.__rows: List[Row] = []
        self.__columns: Dict[str, Column] = {}

        if type(data) is dict:
            # Column Storage
            for key, value in data.items():
                if type(key) is not str:
                    raise TypeError("key should be str")
                if type(value) is not list and type(value) is not tuple:
                    raise TypeError("column should be list")
                self.__columns[key] = Column(key, value)
            # save as rows
            max_column_item_count = 0
            column_name_list = []
            for key, column in self.__columns.items():
                if column.get_length_of_values() > max_column_item_count:
                    max_column_item_count = column.get_length_of_values()
                column_name_list.append(key)
            for i in range(max_column_item_count):
                x = {}
                for column_name in column_name_list:
                    x[column_name] = self.__columns[column_name].get_value_at_index(i)
                self.__rows.append(Row(i, x))

        if type(data) is list or type(data) is tuple:
            # Row Storage
            i = 0
            for datum in data:
                if type(datum) is not dict:
                    raise TypeError("row should be dict")
                self.__rows.append(Row(i, datum))
                i += 1
            # save as columns
            all_column_name_set = set()
            for row in self.__rows:
                x = row.get_defined_key_set()
                all_column_name_set = all_column_name_set.union(x)
            for column_name in all_column_name_set:
                column_value_list = []
                for row_index in range(len(self.__rows)):
                    column_value_list.append(self.__rows[row_index].get_value_for_key(column_name))
                self.__columns[column_name] = Column(column_name, column_value_list)

    def get_a_copy(self):
        data = []
        for row in self.__rows:
            data.append(row.get_raw_row_dict())
        return Matrix(data)

    def get_column_with_name(self, column_name: str):
        return self.__columns[column_name]

    def get_row_with_index(self, index: int):
        return self.__rows[index]

    def get_column_name_set(self):
        x = self.__columns.keys()
        y = set()
        for z in x:
            y.add(z)
        return y

    def get_column_name_tuple(self):
        x = self.__columns.keys()
        y = []
        for z in x:
            y.append(z)
        return tuple(y)

    def get_total_row_count(self):
        return len(self.__rows)

    def get_sub_matrix(
            self,
            column_name_list: List[str] = None,
            conditions: List[Condition] = None,
            index_list: List[int] = None
    ):
        if index_list is None:
            index_list = range(self.get_total_row_count())
        if column_name_list is None:
            column_name_list = self.get_column_name_tuple()

        temp_data = []

        for index in index_list:
            row = self.get_row_with_index(index)

            if conditions is not None:
                metched_all_conditions = True
                for condition in conditions:
                    if not condition.compute_with_row(row):
                        metched_all_conditions = False
                    if not metched_all_conditions:
                        break

                if not metched_all_conditions:
                    continue

            x = {}
            for column_name in column_name_list:
                x[column_name] = row.get_value_for_key(column_name)

            temp_data.append(x)

        return Matrix(temp_data)

    def __str__(self):
        number_length = len(f'self.get_total_row_count()')
        s = "__INDEX".ljust(number_length)
        line = "-" * number_length
        # head
        for column_name in self.get_column_name_tuple():
            s += ' | ' + f'{column_name}'.ljust(self.get_column_with_name(column_name).get_max_char_count())
            line += '-|-' + f'-' * (self.get_column_with_name(column_name).get_max_char_count())
        s += "\n" + line + "\n"
        # body
        for i in range(self.get_total_row_count()):
            row = self.get_row_with_index(i)
            s += f"{row.get_row_index()}".ljust(number_length)
            for column_name in self.get_column_name_tuple():
                s += ' | ' + f'{row.get_value_for_key(column_name)}'.ljust(
                    self.get_column_with_name(column_name).get_max_char_count()
                )
            s += "\n"
        return s

    def update_cell(self, index: int, column_name: str, new_value):
        self.get_row_with_index(index).update_cell(column_name, new_value)
        self.get_column_with_name(column_name).update_cell(index, new_value)
        return self

    def append_one_row(self, row_dict: dict):
        r = {}
        for k in self.get_column_name_tuple():
            r[k] = row_dict[k]
        self.__rows.append(Row(self.get_total_row_count(), r))

        for k in self.get_column_name_tuple():
            self.get_column_with_name(k).append_value(r[k])

        return self

    def append_one_column(self, column_name: str, value_list: list):
        self.__columns[column_name] = Column(column_name, value_list)

        for i in range(self.get_total_row_count()):
            row = self.get_row_with_index(i)
            row.get_raw_row_dict()[column_name] = value_list[i]

        return self
