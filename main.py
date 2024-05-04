import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pyVistaPlot as pvl


def main():
    root = tk.Tk()

    root.geometry("800x600")

    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(expand=True, fill='both')

    # Поле Entry для ввода названия поля для удаления из датасета
    entry_label = tk.Label(main_frame, text="Введите поле для удаления из датасета:", font=12, background='green', foreground='white')
    entry_label.pack(pady=10)

    entry_field = tk.Entry(main_frame, width=60, font=12, background='yellow', foreground='black')
    entry_field.pack()

    # Фрейм для отображения head загруженного датасета
    data_frame = tk.Frame(main_frame, bg='white')
    data_frame.pack(expand=True, fill='both', pady=10)

    # Создаем Listbox для отображения данных
    listbox = tk.Listbox(data_frame, width=50, font=10)
    listbox.pack(expand=True, fill='both', padx=10, pady=10)

    # Кнопка для выбора файла и отображения заголовков
    select_button = tk.Button(main_frame, text="Select File", command=lambda: select_file(main_frame, listbox), width=20, height=3, background='blue', foreground='white', font=("Helvetica", 12))
    select_button.pack(pady=10) 

    # Кнопка для создания графика
    graph_button = tk.Button(main_frame, text="Create Graph", command=lambda: create_graph(data_frame), width=20, height=3, background='green', foreground='white', font=("Helvetica", 12))
    graph_button.pack(pady=10)

    # Устанавливаем конфигурацию для центрирования кнопки
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)

    root.mainloop()

def load_file_once():
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    file_path = filedialog.askopenfilename()
    if file_path:  # Убедиться, что пользователь выбрал файл
        data = pvl.load_file(file_path)  # Загрузить данные из файла
        return data  # Вернуть данные
    return None  # Если файл не был выбран, вернуть None

def select_file(data_frame, listbox):
    data = load_file_once()
    if data is not None:
        header = data.head().reset_index(drop=True)  # Получить заголовки из загруженного датасета
        update_data_frame(data_frame, listbox, header)  # Обновить текст Label в data_frame

def create_graph(data_frame):
    data = load_file_once()
    if data is not None:
        filtered_data = pvl.filter_data(data)  # Применить фильтрацию к данным
        pvl.make_3d_graph(*filtered_data)  # Создать 3D график на основе отфильтрованных данных

def update_data_frame(frame, listbox, header):
    # Очистить фрейм от предыдущего содержимого
    listbox.delete(0, tk.END)

    # Определяем допустимые столбцы для отображения
    valid_columns = [column for column in header.columns if column.isidentifier()]

    # Создаем заголовок
    header_string = " ".join(valid_columns)
    listbox.insert(tk.END, header_string)

    # Определение ширины каждого столбца
    column_widths = [max(len(str(row[column])) for _, row in header.iterrows()) for column in valid_columns]

    # Добавляем данные
    for _, row in header.iterrows():
        row_string = "  ".join(f"{row[column]:<{width}}" for column, width in zip(valid_columns, column_widths))
        listbox.insert(tk.END, row_string)

if __name__ == "__main__":
    main()
