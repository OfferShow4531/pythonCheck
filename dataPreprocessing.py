from tkinter import filedialog, messagebox
import tkinter as tk
import pandas as pd
from pyVistaPlot import Plot

class DataPreprocessing:
    def __init__(self):
        self.data = None
        self.plot = Plot()
    
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

    def save_model(self):
        """Сохранение текущей 3D модели в файл."""
        try:
            self.plot.save_current_model()
            messagebox.showinfo("Успех", "Модель успешно сохранена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить модель: {e}")

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