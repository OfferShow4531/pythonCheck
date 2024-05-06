class DataDescriptor:
    def __init__(self, initial_value=None):
        self._data = initial_value

    def __get__(self, instance, owner):
        return self._data

    def __set__(self, instance, value):
        print("Updating data...")
        self._data = value