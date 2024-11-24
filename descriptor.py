import pandas as pd

class DataDescriptor:
    def __init__(self, initial_value=None):
        self._data = initial_value

    def __get__(self, instance, owner):
        # print(f"Getting data for {instance}")
        return self._data

    def __set__(self, instance, value):
        if isinstance(value, pd.DataFrame):
            # print("Setting data...")
            self._data = value
        else:
            raise ValueError("Assigned value must be a pandas DataFrame.")