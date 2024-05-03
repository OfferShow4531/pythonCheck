import tkinter as tk
import numpy as np
import pandas as pd
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


    min_value = np.amin(data)
    max_value = np.partition(np.unique(data.flatten().round(decimals=10)), -1)[-2]

    return data, min_value, max_value


def main():
    root = tk.Tk()

    main_frame = tk.Frame(root, width=500, height=500, bg='white')
    main_frame.pack(expand=True, fill='both')

    # Кнопка для выбора файла
    select_button = tk.Button(main_frame, text="Select File", command=load_and_process_data)
    select_button.grid(row=0, column=0, padx=20, pady=20)

    # Устанавливаем конфигурацию для центрирования кнопки
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    root.mainloop()

def load_and_process_data():
    file_path = select_file()
    data, min_value, max_value = format_data(file_path)

    # Отображение интерфейса для ввода координат после загрузки файла
    show_input_interface(data, min_value, max_value)

def show_input_interface(data, min_value, max_value):
    root = tk.Toplevel()

    # Ввод координат
    xmin_label = tk.Label(root, text="xmin:")
    xmin_label.grid(row=0, column=0)
    xmin_entry = tk.Entry(root)
    xmin_entry.grid(row=0, column=1)

    xmax_label = tk.Label(root, text="xmax:")
    xmax_label.grid(row=1, column=0)
    xmax_entry = tk.Entry(root)
    xmax_entry.grid(row=1, column=1)

    ymin_label = tk.Label(root, text="ymin:")
    ymin_label.grid(row=2, column=0)
    ymin_entry = tk.Entry(root)
    ymin_entry.grid(row=2, column=1)

    ymax_label = tk.Label(root, text="ymax:")
    ymax_label.grid(row=3, column=0)
    ymax_entry = tk.Entry(root)
    ymax_entry.grid(row=3, column=1)

    c_label = tk.Label(root, text="Insert a number to edit scale bar levels:")
    c_label.grid(row=4, column=0)
    c = tk.Entry(root)
    c.grid(row=4, column=1)

    cmap_label = tk.Label(root, text="cmap:")
    cmap_label.grid(row=5, column=0)
    cmap = tk.Entry(root)
    cmap.grid(row=5, column=1)

    clbwidth_label = tk.Label(root, text="clbwidth:")
    clbwidth_label.grid(row=6, column=0)
    clbwidth = tk.Entry(root)
    clbwidth.grid(row=6, column=1)

    clblabel_label = tk.Label(root, text="clblabel:")
    clblabel_label.grid(row=7, column=0)
    clblabel = tk.Entry(root)
    clblabel.grid(row=7, column=1)

    axislabelsize_label = tk.Label(root, text="axislabelsize:")
    axislabelsize_label.grid(row=8, column=0)
    axislabelsize = tk.Entry(root)
    axislabelsize.grid(row=8, column=1)


    ticklabelsize_label = tk.Label(root, text="ticklabelsize:")
    ticklabelsize_label.grid(row=9, column=0)
    ticklabelsize = tk.Entry(root)
    ticklabelsize.grid(row=9, column=1)


    scalebarsize_label = tk.Label(root, text="scalebarsize:")
    scalebarsize_label.grid(row=10, column=0)
    scalebarsize = tk.Entry(root)
    scalebarsize.grid(row=10, column=1)


    title_label = tk.Label(root, text="title:")
    title_label.grid(row=11, column=0)
    title = tk.Entry(root)
    title.grid(row=11, column=1)


    azim_label = tk.Label(root, text="azim:")
    azim_label.grid(row=12, column=0)
    azim = tk.Entry(root)
    azim.grid(row=12, column=1)


    elev_label = tk.Label(root, text="elev:")
    elev_label.grid(row=13, column=0)
    elev = tk.Entry(root)
    elev.grid(row=13, column=1)


    name_label = tk.Label(root, text="name:")
    name_label.grid(row=14, column=0)
    name = tk.Entry(root)
    name.grid(row=14, column=1)


    filetype_label = tk.Label(root, text="filetype:")
    filetype_label.grid(row=15, column=0)
    filetype = tk.Entry(root)
    filetype.grid(row=15, column=1)
 

    dpi_label = tk.Label(root, text="dpi:")
    dpi_label.grid(row=16, column=0)
    dpi = tk.Entry(root)
    dpi.grid(row=16, column=1)


    submit_button = tk.Button(root, text="Submit", command=lambda: make_3D_visualization(data, min_value, max_value, xmin_entry.get(), xmax_entry.get(), ymin_entry.get(), ymax_entry.get(), int(c.get()), cmap.get(), int(clbwidth.get()), clblabel.get(), int(axislabelsize.get()), int(ticklabelsize.get()), int(scalebarsize.get()), title.get(), int(azim.get()), int(elev.get()), name.get(), filetype.get(), int(dpi.get())))
    submit_button.grid(row=17, column=1)

def make_3D_visualization(data, a, b, xmin, xmax, ymin, ymax, c, cmap, clbwidth, clblabel, axislabelsize, ticklabelsize, scalebarsize, title, azim, elev, name, filetype, dpi):
    # Создаем сетку координат x и y на основе введенных значений
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
