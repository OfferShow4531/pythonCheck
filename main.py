import tkinter as tk #Tkinter
from tkinter import filedialog, messagebox
import pandas as pd
from pyVistaPlot import Plot

class Main:
    def __init__(self):
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
        # self.save_button = tk.Button(self.left_frame, text="Сохранить модель", command=self.save_model)
        # self.save_button.pack(pady=5)

        self.root.mainloop()

    def load_file(self):
        """Загрузка CSV файла с данными."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                timestamps = self.data['Timestamp'].unique()

                # Обновление меню выбора Timestamp
                self.timestamp_menu['menu'].delete(0, 'end')
                self.timestamp_var.set('')

                for timestamp in timestamps:
                    self.timestamp_menu['menu'].add_command(
                        label=str(timestamp),
                        command=tk._setit(self.timestamp_var, str(timestamp))
                    )
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def create_3d_model(self):
        """Создание 3D модели для выбранного Timestamp."""
        if not self.data_is_loaded():
            return
        
        timestamp = self.get_selected_timestamp()
        if timestamp is None:
            return

        try:
            # Фильтрация данных и создание графика
            filtered_data = self.plot.filter_data(self.data, timestamp)
            self.plot.make_3d_graph(*filtered_data)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать модель: {e}")

    def animate_model(self):
        """Анимация для всех доступных Timestamp."""
        if not self.data_is_loaded():
            return

        for timestamp in self.data['Timestamp'].unique():
            try:
                filtered_data = self.plot.filter_data(self.data, timestamp)
                self.plot.make_3d_graph(*filtered_data)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Анимация прервана: {e}")
                break



    def data_is_loaded(self):
        """Проверка, загружены ли данные."""
        if self.data is None:
            messagebox.showwarning("Ошибка", "Загрузите данные перед продолжением.")
            return False
        return True

    def get_selected_timestamp(self):
        """Получает выбранный Timestamp."""
        timestamp_str = self.timestamp_var.get()
        if not timestamp_str:
            messagebox.showwarning("Ошибка", "Выберите timestamp.")
            return None
        try:
            return float(timestamp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат timestamp.")
            return None

if __name__ == "__main__":
    Main()