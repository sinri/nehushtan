import importlib


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_target(target, keychain: tuple, default: any = None):
        if type(target) is dict:
            return CommonHelper.read_dictionary(target, keychain, default)
        elif type(target) is list or type(target) is tuple:
            return CommonHelper.read_array(target, keychain, default)
        else:
            return default

    @staticmethod
    def read_dictionary(dictionary: dict, keychain: tuple, default: any = None):
        if len(keychain) <= 0:
            return default
        elif len(keychain) == 1:
            return dictionary.get(keychain[0], default)
        else:
            current_key = keychain[0]
            if dictionary.keys().__contains__(current_key):
                sub_dictionary = dictionary.get(current_key, None)
                if type(sub_dictionary) is dict:
                    return CommonHelper.read_dictionary(sub_dictionary, keychain[1:], default)
                elif type(sub_dictionary) is tuple or type(sub_dictionary) is list:
                    return CommonHelper.read_array(sub_dictionary, keychain[1:], default)
                else:
                    return default
            else:
                return default

    @staticmethod
    def read_array(array: tuple, keychain: tuple, default: any = None):
        if len(keychain) <= 0:
            return default
        elif len(keychain) == 1:
            current_key = int(keychain[0])
            if len(array) > current_key:
                return array[int(keychain[0])]
            else:
                return default
        else:
            current_key = int(keychain[0])
            if len(array) > current_key:
                sub_array = array[current_key]
                if type(sub_array) is tuple or type(sub_array) is list:
                    return CommonHelper.read_array(sub_array, keychain[1:], default)
                elif type(sub_array) is dict:
                    return CommonHelper.read_dictionary(sub_array, keychain[1:], default)
                else:
                    return default
            else:
                return default

    @staticmethod
    def write_dictionary(target_dict: dict, keychain: tuple, value: any):
        if len(keychain) <= 0:
            # not modify anything if keychain is empty
            return target_dict
        if len(keychain) == 1:
            target_dict[keychain[0]] = value
            return target_dict

        current_key = keychain[0]
        if target_dict.get(current_key) is None:
            target_dict[current_key] = {}
        return CommonHelper.write_dictionary(target_dict[current_key], keychain[1:], value)

    @staticmethod
    def class_with_class_path(class_path: str):
        """
        Since 0.1.21
        For a/b.py -> class b
        class_with_namespace is like 'package.sub_package.class', 'a.b'
        return a CLASS definition, to be used with parameters to make instance
        """
        module = importlib.import_module(class_path)
        a_class = getattr(module, class_path)
        return a_class

    @staticmethod
    def class_with_module_and_name(module_base: str, sub_module_name: str):
        """
        Since 0.1.21
        For a/b.py -> class b
        module_base is a
        sub_module_name is b
        """
        module = __import__(module_base)
        a_class = getattr(module, sub_module_name)
        return a_class
