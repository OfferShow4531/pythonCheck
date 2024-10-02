import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import filedialog, messagebox
from pyVistaPlot import Plot


import tkinter as tk

class Main:
    def __init__(self):
        self.file_path = None
        self.data = None  # DataFrame для хранения данных
        self.plot = Plot()  # Класс для работы с 3D графикой

        # Создание главного окна
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("3D Модель Скважин")

        # Фреймы для размещения виджетов
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        self.left_frame = tk.Frame(self.main_frame, bg='lightgray')
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Кнопка выбора файла
        self.select_file_button = tk.Button(self.left_frame, text="Выбрать файл", command=self.load_file)
        self.select_file_button.pack(pady=5)

        # Опции для выбора Timestamp
        self.timestamp_var = tk.StringVar()
        self.timestamp_menu = tk.OptionMenu(self.left_frame, self.timestamp_var, "")
        self.timestamp_menu.pack(pady=5)

        # Кнопка для создания 3D модели
        self.create_graph_button = tk.Button(self.left_frame, text="Создать 3D модель", command=self.create_3d_model)
        self.create_graph_button.pack(pady=5)

        # Кнопка для анимации Timestamp
        self.animate_button = tk.Button(self.left_frame, text="Анимация", command=self.animate_model)
        self.animate_button.pack(pady=5)

        # Кнопка сохранения
        self.save_button = tk.Button(self.left_frame, text="Сохранить модель", command=self.save_model)
        self.save_button.pack(pady=5)

        self.root.mainloop()

    def load_file(self):
        """Загрузка CSV файла с данными"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            if 'Timestamp' not in self.data.columns or 'Xpos' not in self.data.columns or 'Ypos' not in self.data.columns:
                messagebox.showerror("Ошибка", "CSV файл должен содержать столбцы 'Timestamp', 'Xpos' и 'Ypos'.")
                return

            timestamps = self.data['Timestamp'].unique()
            self.timestamp_menu['menu'].delete(0, 'end')
            self.timestamp_var.set('')  # Сбрасываем текущее значение
            for timestamp in timestamps:
                self.timestamp_menu['menu'].add_command(label=str(timestamp), command=tk._setit(self.timestamp_var, str(timestamp)))

    def create_3d_model(self):
        """Создание 3D модели для выбранного Timestamp"""
        if self.data is not None:
            timestamp_str = self.timestamp_var.get()
            if not timestamp_str:  # Проверка на пустое значение
                messagebox.showwarning("Ошибка", "Выберите timestamp.")
                return
            
            try:
                timestamp = float(timestamp_str)
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат timestamp.")
                return

            filtered_data = self.plot.filter_data(self.data, timestamp)
            if filtered_data is not None:
                self.plot.make_3d_graph(*filtered_data)
            else:
                messagebox.showwarning("Предупреждение", "Нет данных для выбранного timestamp.")

    def animate_model(self):
        """Анимация для каждого Timestamp"""
        if self.data is not None:
            timestamps = self.data['Timestamp'].unique()
            for timestamp in timestamps:
                filtered_data = self.plot.filter_data(self.data, timestamp)
                if filtered_data is not None:
                    self.plot.make_3d_graph(*filtered_data)

    def save_model(self):
        """Сохранение текущей модели в файл"""
        self.plot.save_current_model()

if __name__ == "__main__":
    Main()