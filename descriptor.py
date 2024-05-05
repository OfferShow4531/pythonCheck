class DataDescriptor:
    def __init__(self, initial_value=None):
        self._data = initial_value

    def __get__(self, instance, owner):
        return self._data

    def __set__(self, instance, value):
        # В этом примере мы можем добавить дополнительную логику
        # для обновления данных в другом файле или любой другой логики,
        # которая должна быть выполнена при изменении параметра
        print("Updating data...")
        self._data = value
