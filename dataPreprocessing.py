import pandas as pd
from tkinter import filedialog
from descriptor import DataDescriptor

class DataPreprocessing:
    data = DataDescriptor()  # Используем DataDescriptor для атрибута data

    def __init__(self):
        self.data = None  # Инициализация атрибута data через DataDescriptor
        self.timestamps = []  # Хранение доступных timestamp значений

    def load_file(self):
        """Загружает данные из выбранного файла и обновляет timestamps."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.data = pd.read_csv(file_path)  # При изменении self.data вызовется DataDescriptor
            print("Файл загружен успешно")
            self.update_timestamps()  # Обновляем timestamps после загрузки файла

    def update_timestamps(self):
        """Обновляет уникальные значения timestamps при загрузке нового файла."""
        if self.data is not None:
            self.timestamps = sorted(self.data['Timestamp'].unique())
            print("Доступные timestamps:", self.timestamps)

    def get_filtered_data(self, timestamp):
        """Фильтрует данные по Timestamp и возвращает координаты для визуализации."""
        if self.data is None:
            raise ValueError("Данные не загружены")

        filtered_data = self.data[self.data['Timestamp'] == int(timestamp)]
        if filtered_data.empty:
            raise ValueError(f"Нет данных для timestamp {timestamp}")

        x_coordinate = filtered_data['Xpos'].values[0]
        y_coordinate = filtered_data['Ypos'].values[0]
        z_coordinates = filtered_data[['Well1', 'Well2', 'Well3', 'Well4', 'Well5', 'Well6', 'Well7', 'Well8', 'Well9', 'Well10']].values.T
        n_wells = z_coordinates.shape[0]
        return x_coordinate, y_coordinate, z_coordinates, n_wells