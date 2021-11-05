class Row:
    def __init__(self, index: int, row_dict: dict):
        self.__index = index
        self.__row_dict = row_dict

    def get_row_index(self):
        return self.__index

    def get_value_for_key(self, key: str):
        return self.__row_dict.get(key)

    def get_defined_key_set(self):
        x = self.__row_dict.keys()
        y = set()
        for z in x:
            y.add(z)
        return y

    def get_raw_row_dict(self):
        return self.__row_dict

    def update_cell(self, column_name: str, value):
        if column_name not in self.get_defined_key_set():
            raise KeyError('update target column name not defined in row')
        self.__row_dict[column_name] = value
        return self
