import tkinter as tk
import numpy as np
import pandas as pd
from random import random
from random_value import get_options_value
import pyvista as pv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tkinter import simpledialog, filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    file_path = filedialog.askopenfilename()
    return file_path

def format_data(file_path):
    data = pd.read_csv(file_path, header=None)

    # Преобразование данных в массив NumPy
    data = np.array(data)

    flattened_data = data.flatten()  # Выравнивание данных до одной оси

    # Учитываем разные форматы данных
    if np.issubdtype(data.dtype, np.number):  # Если данные числового формата
        min_value = np.amin(flattened_data)
        max_value = np.partition(np.unique(flattened_data), -1)[-2]
    elif np.issubdtype(data.dtype, np.bool_):  # Если данные логического формата
        min_value = False
        max_value = True
    else:  # Если данные текстового формата
        min_value = None
        max_value = None

    return data, min_value, max_value

def main():
    root = tk.Tk()

    root.geometry("250x250")

    main_frame = tk.Frame(root, width=100, height=150, bg='white')
    main_frame.pack(expand=True, fill='both')

    # Кнопка для выбора файла
    select_button = tk.Button(main_frame, text="Select File", command=load_and_process_data, width=20, height=3, background='blue', foreground='white', font=16)
    select_button.pack(expand=True)

    # Устанавливаем конфигурацию для центрирования кнопки
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    root.mainloop()


def load_and_process_data():
    file_path = select_file()
    data, min_value, max_value = format_data(file_path)

    # Отображение интерфейса для ввода координат после загрузки файла
    show_input_interface(data, min_value, max_value)

# def show_input_interface(data, min_value, max_value):
#     root = tk.Toplevel()

#     # Ввод координат
#     xmin_label = tk.Label(root, text="xmin:")
#     xmin_label.grid(row=0, column=0)
#     xmin_entry = tk.Entry(root)
#     xmin_entry.grid(row=0, column=1)

#     xmax_label = tk.Label(root, text="xmax:")
#     xmax_label.grid(row=1, column=0)
#     xmax_entry = tk.Entry(root)
#     xmax_entry.grid(row=1, column=1)

#     ymin_label = tk.Label(root, text="ymin:")
#     ymin_label.grid(row=2, column=0)
#     ymin_entry = tk.Entry(root)
#     ymin_entry.grid(row=2, column=1)

#     ymax_label = tk.Label(root, text="ymax:")
#     ymax_label.grid(row=3, column=0)
#     ymax_entry = tk.Entry(root)
#     ymax_entry.grid(row=3, column=1)

#     c_label = tk.Label(root, text="Insert a number to edit scale bar levels:")
#     c_label.grid(row=4, column=0)
#     c = tk.Entry(root)
#     c.grid(row=4, column=1)

#     cmap_label = tk.Label(root, text="cmap:")
#     cmap_label.grid(row=5, column=0)
#     cmap = tk.Entry(root)
#     cmap.grid(row=5, column=1)

#     clbwidth_label = tk.Label(root, text="clbwidth:")
#     clbwidth_label.grid(row=6, column=0)
#     clbwidth = tk.Entry(root)
#     clbwidth.grid(row=6, column=1)

#     clblabel_label = tk.Label(root, text="clblabel:")
#     clblabel_label.grid(row=7, column=0)
#     clblabel = tk.Entry(root)
#     clblabel.grid(row=7, column=1)

#     axislabelsize_label = tk.Label(root, text="axislabelsize:")
#     axislabelsize_label.grid(row=8, column=0)
#     axislabelsize = tk.Entry(root)
#     axislabelsize.grid(row=8, column=1)


#     ticklabelsize_label = tk.Label(root, text="ticklabelsize:")
#     ticklabelsize_label.grid(row=9, column=0)
#     ticklabelsize = tk.Entry(root)
#     ticklabelsize.grid(row=9, column=1)


#     scalebarsize_label = tk.Label(root, text="scalebarsize:")
#     scalebarsize_label.grid(row=10, column=0)
#     scalebarsize = tk.Entry(root)
#     scalebarsize.grid(row=10, column=1)


#     title_label = tk.Label(root, text="title:")
#     title_label.grid(row=11, column=0)
#     title = tk.Entry(root)
#     title.grid(row=11, column=1)


#     azim_label = tk.Label(root, text="azim:")
#     azim_label.grid(row=12, column=0)
#     azim = tk.Entry(root)
#     azim.grid(row=12, column=1)


#     elev_label = tk.Label(root, text="elev:")
#     elev_label.grid(row=13, column=0)
#     elev = tk.Entry(root)
#     elev.grid(row=13, column=1)


#     name_label = tk.Label(root, text="name:")
#     name_label.grid(row=14, column=0)
#     name = tk.Entry(root)
#     name.grid(row=14, column=1)


#     filetype_label = tk.Label(root, text="filetype:")
#     filetype_label.grid(row=15, column=0)
#     filetype = tk.Entry(root)
#     filetype.grid(row=15, column=1)
 

#     dpi_label = tk.Label(root, text="dpi:")
#     dpi_label.grid(row=16, column=0)
#     dpi = tk.Entry(root)
#     dpi.grid(row=16, column=1)


#     submit_button = tk.Button(root, text="Submit", command=lambda: make_3D_visualization(data, min_value, max_value, xmin_entry.get(), xmax_entry.get(), ymin_entry.get(), ymax_entry.get(), int(c.get()), cmap.get(), int(clbwidth.get()), clblabel.get(), int(axislabelsize.get()), int(ticklabelsize.get()), int(scalebarsize.get()), title.get(), int(azim.get()), int(elev.get()), name.get(), filetype.get(), int(dpi.get())))
#     submit_button.grid(row=17, column=1)


def show_input_interface(data, min_value, max_value):
    root = tk.Toplevel()

    root.geometry("600x800")
    root['padx'] = 15 
    root['pady'] = 15 
    # Ввод координат
    fields = ["xmin", "xmax", "ymin", "ymax", "c", "cmap", "clbwidth", "clblabel", "axislabelsize", "ticklabelsize", "scalebarsize", "azim", "elev", "filetype", "dpi"]

    # Создаем стиль для Label
    label_style = {'font': ('Times New Roman', 16), 'background': 'blue', 'foreground': 'white', 'width': 15, 'padx': 15}

    variables = {}

    filetype_values = ["png", "jpg", "shp"]
    dpi_values = [300, 600, 1200]

    for i, field in enumerate(fields):
        label = tk.Label(root, text=field + ":", **label_style)
        label.grid(row=i, column=0)

        # Генерация значений для выпадающих списков
        if field == "dpi":
            values = dpi_values
        elif field == "filetype":
            values = filetype_values
        else:
            values = sorted([get_options_value(field) for _ in range(5)])

        variable = tk.StringVar(root)
        variable.set(values[0])  # Значение по умолчанию

        # Создаем стиль для OptionMenu
        option_style = {'font': ('Times New Roman', 16), 'background': 'blue', 'foreground': 'white', 'width': 15}

        def on_option_selected(*args):
            option_menu.config(bg='green')

        variable.trace_add('write', on_option_selected)

        option_menu = tk.OptionMenu(root, variable, *values)
        option_menu.config(**option_style)
        option_menu.grid(row=i, column=1)
        
        # Добавляем переменные dpi и filetype в variables
        if field == "dpi":
            variables["dpi"] = variable
        elif field == "filetype":
            variables["filetype"] = variable
        else:
            # Добавляем все другие переменные StringVar в variables
            variables[field] = variable

    # Entry для поля title
    tk.Label(root, text="title:", **label_style).grid(row=len(fields), column=0)
    title_var = tk.StringVar(root)
    title_entry = tk.Entry(root, textvariable=title_var, width=30)  # Увеличиваем ширину до 30 символов
    title_entry.grid(row=len(fields), column=1)

    # Entry для поля name
    tk.Label(root, text="name:", **label_style).grid(row=len(fields)+1, column=0)
    name_var = tk.StringVar(root)
    name_entry = tk.Entry(root, textvariable=name_var, width=30)  # Увеличиваем ширину до 30 символов
    name_entry.grid(row=len(fields)+1, column=1)

    # Добавляем переменные title и name в variables
    variables["title"] = title_var
    variables["name"] = name_var


    for key, value in variables.items():
        print(f"{key}: {value}")
    
    print(min_value, max_value)

    button_style = {'font': ('Times New Roman', 16), 'background': 'blue', 'foreground': 'white', 'width': 30}

    submit_button = tk.Button(root, text="Submit", command=lambda: make_3D_visualization(data, min_value, max_value *[variable.get() for variable in variables.values() if isinstance(variable, tk.StringVar)]), **button_style)
    submit_button.grid(row=len(fields)+2, column=0, columnspan=2, pady=10)

def make_3D_visualization(data, a, b, xmin, xmax, ymin, ymax, c, cmap, clbwidth, clblabel, axislabelsize, ticklabelsize, scalebarsize, title, azim, elev, name, filetype, dpi):
    # Создаем сетку координат x и y на основе введенных значений
    # Находим индекс столбца "timeStamp"
    # timestamp_index = np.where(data[0] == 'timeStamp')[0][0]

    # # Удаляем столбец "timeStamp"
    # data_without_timestamp = np.delete(data, timestamp_index, axis=1)

    
    # Преобразуем данные в массив NumPy
    # data_edited = np.array([line.split(',') for line in data_without_timestamp.split('\n')])

    # Преобразуем строки в числовые значения, если это возможно
    # try:
    #     print("Тип данных до преобразования:", type(data_edited))
    #     data_edited = data_edited.astype(float)
    #     print("Тип данных после преобразования:", type(data_edited))
    #     print(data_edited)
    # except ValueError:
    #     print("Ошибка: Невозможно преобразовать данные в числовой формат.")
    

    # Преобразуем остальные параметры к числовому типу
    # xmin = float(xmin)
    # xmax = float(xmax)
    # ymin = float(ymin)
    # ymax = float(ymax)
    # azim = int(azim)
    # elev = int(elev)


    x = np.linspace(float(xmin), float(xmax), data.shape[1])
    y = np.linspace(float(ymin), float(ymax), data.shape[0])

    X, Y = np.meshgrid(x, y)
    # Создаем объект Grid с помощью pyvista
    grid = pv.StructuredGrid(X, Y, np.zeros_like(data))

    # Получаем координаты узлов сетки
    points = grid.points

    # Создаем пустой массив данных для каждого узла сетки
    grid_data = np.zeros(points.shape[0])

    # Заполняем массив данных значениями из исходных данных
    for i in range(points.shape[0]):
        grid_data[i] = data[i // data.shape[1], i % data.shape[1]]
    
    print(grid_data)

    # Добавляем массив данных к сетке
    grid.point_data['data'] = grid_data

    # Создаем окно для отображения
    plotter = pv.Plotter()

    # Добавляем сетку к окну
    plotter.add_mesh(grid, scalars='data', cmap=cmap, clim=[a, b])

    # Настраиваем цветовую шкалу
    plotter.add_scalar_bar(title=clblabel, width=clbwidth, label_font_size=scalebarsize)
    # Устанавливаем подписи к осям и заголовок
    plotter.xlabel = 'Latitude'
    plotter.ylabel = 'Longitude'
    plotter.zlabel = clblabel
    plotter.title = title

    # Устанавливаем углы обзора
    plotter.camera.azimuth = azim
    plotter.camera.elevation = elev
    plotter.show()

    # Сохраняем изображение
    plotter.screenshot(name + '.' + filetype, transparent_background=True, scale=dpi)

    # Закрываем окно с графиком
    plotter.close()

if __name__ == "__main__":
    main()
