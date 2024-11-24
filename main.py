import tkinter as tk
from dataPreprocessing import DataPreprocessing
from pyVistaPlot import Plot3D
from pyVista2DPlot import Plot2D

class Main:
    def __init__(self):
        self.dataPreproc = DataPreprocessing()
        # self.plot = Plot3D()
        # self.plot2D = Plot2D()
        
        # Создание главного окна
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("3D Модель Скважин")

        # Фреймы для размещения виджетов
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        self.left_frame = tk.Frame(self.main_frame, bg='lightgray')
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Кнопка выбора файла
        self.select_file_button = tk.Button(self.left_frame, text="Выбрать файл", command=self.load_and_prepare_data)
        self.select_file_button.pack(pady=5)

        # Опции для выбора Timestamp
        self.timestamp_var = tk.StringVar(value="Выберите timestamp")  # Устанавливаем значение по умолчанию
        self.timestamp_menu = tk.OptionMenu(self.left_frame, self.timestamp_var, "")
        self.timestamp_menu.pack(pady=5)

        # Кнопка для создания 3D модели
        self.create_graph_button = tk.Button(self.left_frame, text="Создать 3D модель", command=self.create_model)
        self.create_graph_button.pack(pady=5)
        
        self.create_2d_button = tk.Button(self.left_frame, text="Создать 2D модель", command=self.create_2d_model)
        self.create_2d_button.pack(pady=5)

        # Кнопка для анимации Timestamp
        self.animate_button = tk.Button(self.left_frame, text="Анимация", command=self.animate_model)
        self.animate_button.pack(pady=5)

        # Кнопка сохранения
        self.save_button = tk.Button(self.left_frame, text="Сохранить модель", command=self.save_model)
        self.save_button.pack(pady=5)

        self.root.mainloop()

    def load_and_prepare_data(self):
        """Загружает файл и обновляет меню Timestamp."""
        self.dataPreproc.load_file()
        
        # Очистка и обновление timestamp_menu
        self.timestamp_menu["menu"].delete(0, "end")
        if self.dataPreproc.timestamps:
            # Устанавливаем первый элемент как выбранный по умолчанию
            self.timestamp_var.set(self.dataPreproc.timestamps[0])

            # Добавляем timestamps в меню
            for timestamp in self.dataPreproc.timestamps:
                self.timestamp_menu["menu"].add_command(
                    label=timestamp, command=tk._setit(self.timestamp_var, timestamp)
                )
            
            # Обновляем виджет OptionMenu
            self.timestamp_menu.update()  # Обновление виджета для отображения изменений

    def create_model(self):
        """Создает 3D модель для выбранного Timestamp"""
        timestamp = self.timestamp_var.get()
        if timestamp and timestamp != "Выберите timestamp":
            x, y, z, n_wells = self.dataPreproc.get_filtered_data(timestamp)
            self.plot.make_3d_model(x, y, z, n_wells)
        else:
            print("Выберите timestamp для создания модели")
    
    def create_2d_model(self):
        """Создает 3D модель для выбранного Timestamp"""
        timestamp = self.timestamp_var.get()
        if timestamp and timestamp != "Выберите timestamp":
            x, y, z, n_wells = self.dataPreproc.get_filtered_data(timestamp)
            self.plot2D.make_2d_projection(x, y, z, n_wells)
        else:
            print("Выберите timestamp для создания модели")

    def animate_model(self):
        """Запускает анимацию модели"""
        self.plot.animate_rain()

    def save_model(self):
        """Сохраняет текущую 3D модель"""
        self.plot.save_model()

if __name__ == "__main__":
    Main()