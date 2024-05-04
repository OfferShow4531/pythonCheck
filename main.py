import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pyVistaPlot as pvl


import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("800x600")

    main_frame = tk.Frame(root, bg='Slategray2')
    main_frame.pack(expand=True, fill='both')

    # Первое внутреннее окно
    inner_frame = tk.Frame(main_frame, bg='Slategray1')
    inner_frame.pack(expand=True, fill='both', padx=10, pady=(10, 70))  # Увеличиваем нижний отступ для кнопок

    # Полоса серого цвета сверху
    top_bar = tk.Frame(inner_frame, bg='gray', height=15)
    top_bar.pack(fill='x')

    # Разделение на два отдельных окна
    left_frame = tk.Frame(inner_frame, bg='Slategray1')
    left_frame.pack(side='left', expand=True, fill='both')

    right_frame = tk.Frame(inner_frame, bg='Slategray1')
    right_frame.pack(side='right', expand=True, fill='both')

    # left_frame
    label_current_dataset = tk.Label(left_frame, background='Slategray1', text="Current Data Set", font=('Arial', 12, 'bold italic'), anchor='w', highlightthickness=0)
    label_current_dataset.pack(fill='x', padx=10, pady=(10, 5))

    label_count_of_rows = tk.Label(left_frame, background='Slategray1', text="Count of Rows", font=('Arial', 12, 'bold italic'), anchor='w', highlightthickness=0)
    label_count_of_rows.pack(fill='x', padx=10, pady=(5, 10))

    points_frame = tk.Frame(left_frame, bg='white')
    points_frame.pack()

    for _ in range(5):
        point = tk.Label(points_frame, background='Slategray1', text='•', font=('Arial', 30), padx=30, highlightthickness=0)
        point.pack(side='left')


    entry_field = tk.Entry(left_frame, font=14, background='gray', foreground='white')
    entry_field.pack(fill='x', padx=10, pady=30)

    reset_button = tk.Button(left_frame, text="Reset", width=25, height=2, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
    reset_button.pack(padx=10, pady=10)

    load_data_button = tk.Button(left_frame, text="Load Data", width=30, height=3, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
    load_data_button.pack(padx=10, pady=15)

    # right_frame
    listbox = tk.Listbox(right_frame, width=100, font=7, background='gray', foreground='white')
    listbox.pack(expand=True, fill='both', padx=10, pady=10)

    # Кнопки с отступами между ними
    buttons_frame = tk.Frame(main_frame, bg='Slategray2')  # Помещаем кнопки в основной фрейм
    buttons_frame.pack(fill='x', pady=(0, 10))  # Увеличиваем верхний отступ для кнопок

    select_file_button = tk.Button(buttons_frame, text="SELECT FILE", command=lambda: select_file(main_frame, listbox), width=30, height=3, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
    select_file_button.pack(side='left', padx=(10, 5))

    create_graph_button = tk.Button(buttons_frame, text="CREATE GRAPH", command=lambda: create_graph(inner_frame), width=30, height=3, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
    create_graph_button.pack(side='right', padx=(5, 10))

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
