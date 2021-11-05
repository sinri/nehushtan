class Column:
    def __init__(self, column_name: str, values: list):
        self.__column_name = column_name
        self.__values = values
        self.__computed_max_char_count = self.__compute_max_char_count()

    def get_length_of_values(self):
        return len(self.__values)

    def get_column_name(self):
        return self.__column_name

    def get_value_at_index(self, index: int):
        return self.__values[index]

    def get_raw_value_list(self):
        return self.__values

    def __compute_max_char_count(self):
        m = len(self.__column_name)
        for v in self.__values:
            s = f'{v}'
            if len(s) > m:
                m = len(s)
        return m

    def get_max_char_count(self):
        return self.__computed_max_char_count

    def update_cell(self, index: int, value):
        if 0 > index or index >= len(self.__values):
            raise KeyError('update target row index not defined in column')
        self.__values[index] = value
        self.__compute_max_char_count()
        return self

    def append_value(self, value):
        self.__values.append(value)
        return self
