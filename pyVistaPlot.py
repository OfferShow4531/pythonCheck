import numpy as np
import pandas as pd
import pyvista as pv
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import vtk
import itertools
import logging
from pyvista import examples

# Устанавливаем настройки логирования
logging.basicConfig(filename='error.log', level=logging.DEBUG)

class Plot:
    def __init__(self, data_descriptor):
        self.data_descriptor = data_descriptor

    def load_file(self, file):
        data = pd.read_csv(file)


        self.data_descriptor._data = data

        return data

    # def filter_data(self, data):
    #     well_data = self.data_descriptor._data
    #     n_wells = well_data.shape[1] - 3  # Вычитаем 3, так как у нас есть столбцы Timestamp, Xpos и Ypos
    #     x_coordinates = data['Xpos']
    #     y_coordinates = data['Ypos']
    #     z_coordinates = np.array([data[f'Well{i+1}'] for i in range(n_wells)]).T  # Создаем массив Z координат для каждой скважины
    #     timestamps = data['Timestamp']  # Получаем временные метки
    #     return x_coordinates, y_coordinates, z_coordinates, timestamps, n_wells
    
    def filter_data(self, data):
        well_data = self.data_descriptor._data
        n_wells = well_data.shape[1] - 3  # Вычитаем 3, так как у нас есть столбцы Timestamp, Xpos и Ypos
        x_coordinates = data['Xpos']
        y_coordinates = data['Ypos']
        z_coordinates = np.array([data[f'Well{i+1}'] for i in range(n_wells)]).T  # Создаем массив Z координат для каждой скважины
        return x_coordinates, y_coordinates, z_coordinates, n_wells
        # x_coordinates = data['Xpos']  # Используем данные Xpos
        # y_coordinates = data['Ypos']  # Используем данные Ypos

        # Получаем данные для каждого временного шага
        # timestamps = data['Timestamp'].unique()

        # Создаем массив точек (X, Y, Z) для каждого временного шага и каждой скважины
        # points = []
        # for timestamp in timestamps:
        #     for i in range(len(x_coordinates)):
        #         x = x_coordinates[i]
        #         y = y_coordinates[i]
        #         for j in range(n_wells):
        #             well_column_name = f'Well{j + 1}'
        #             if well_column_name in data.columns:
        #                 filtered_data = data.query(f'Xpos == {x} and Ypos == {y} and Timestamp == {timestamp}')
        #                 if not filtered_data.empty:
        #                     z = filtered_data[well_column_name].values[0]
        #                     points.append([x, y, z])
        #                     print(x,y,z)

        # points = np.array(points)
       
    
    # def make_3d_graph(self, points, x_coordinates, y_coordinates, n_weels, well_data, file_type):
    #     x_ground, y_ground = np.meshgrid(x_coordinates, y_coordinates)
        
    #     print("Sizes: x_ground:", x_ground.shape, "y_ground:", y_ground.shape)

    #     print("Sizes: points:", points.shape)

    #     z_ground = points[:, 2].reshape(x_ground.shape)

    #     ground = pv.StructuredGrid(x_ground, y_ground, z_ground)

    #     plotter = pv.Plotter()
    #     plotter.add_mesh(ground, color="green", opacity=0.5, label="Ground")

    #     for column_index in range(n_weels):
    #         column_points = well_data.iloc[:, column_index].values
    #         unique_points, point_counts = np.unique(column_points, return_counts=True)
    #         common_points = unique_points[point_counts > 1]

    #         for point_value in common_points:
    #             point_indices = np.where(column_points == point_value)[0]
    #             # Построение линий только в случае, если координаты точки присутствуют в данных
    #             if len(point_indices) > 0:
    #                 line_points = np.array([points[point_indices[0]], points[point_indices[-1]]])
    #                 plotter.add_lines(line_points, color="blue", width=1)

        # plotter.add_legend(bcolor='w', face=None)

        # min_elevation = np.min(points[:, 2])  # Минимальная высота берется прямо из данных по оси Z
        # max_elevation = np.max(points[:, 2])  # Максимальная высота берется прямо из данных по оси Z
        # plotter.add_text(f"Min: {min_elevation}", position="upper_left", font_size=12)
        # plotter.add_text(f"Max: {max_elevation}", position="lower_left", font_size=12)
        # plotter.show()

    def height_function(self, x, y):
        # Пример функции высоты, можно заменить на любую другую
        return np.sin(x) * np.cos(y)

    # def make_3d_graph(self, x_coordinates, y_coordinates, z_coordinates, timestamps, n_wells, file_type):
    #     # Нормализация координат Z
    #     z_min = np.min(z_coordinates)
    #     z_max = np.max(z_coordinates)
    #     z_range = z_max - z_min
    #     z_normalized = (z_coordinates - z_min) / z_range

    #     plotter = pv.Plotter()

    #     # Создание градиентной цветовой карты для временных меток
    #     cmap = plt.get_cmap('plasma', len(timestamps))
    #     custom_cmap = ListedColormap(cmap(np.linspace(0, 1, len(timestamps))))

    #     # Создание трехмерной поверхности земли
    #     x_ground, y_ground = np.meshgrid(x_coordinates, y_coordinates)
    #     z_ground = self.height_function(x_ground, y_ground)
    #     ground = pv.StructuredGrid(x_ground, y_ground, z_ground)
    #     plotter.add_mesh(ground, color="green", opacity=0.5, label="Ground")

    #     # Добавление скважин
    #     for i in range(n_wells):
    #         well_coordinates = np.column_stack((x_coordinates, y_coordinates, z_normalized[:, i]))
    #         well_polydata = pv.PolyData(well_coordinates)

    #         # Увеличение размера точек и указание различных форм
    #         plotter.add_mesh(well_polydata, color=custom_cmap(i), point_size=15, render_points_as_spheres=True, label=f"Well {i+1}")

    #     # Создание легенды для временных меток
    #     legend_labels = [f"{i+1}: {timestamps[i]}" for i in range(len(timestamps))]
    #     color_bar = plotter.add_scalar_bar(title="Timestamp", n_labels=len(timestamps), height=0.5, vertical=True)

    #     # Настройка цветовой шкалы
    #     lut = vtk.vtkLookupTable()
    #     lut.SetNumberOfTableValues(len(timestamps))
    #     for i, color in enumerate(custom_cmap.colors):
    #         lut.SetTableValue(i, color[0], color[1], color[2], 1.0)
    #     color_bar.SetLookupTable(lut)

    #     # Добавление текста для минимальной и максимальной высоты
    #     min_elevation = np.min(z_coordinates)
    #     max_elevation = np.max(z_coordinates)
    #     plotter.add_text(f"Min Elevation: {min_elevation}", position="upper_left", font_size=12)
    #     plotter.add_text(f"Max Elevation: {max_elevation}", position="lower_left", font_size=12)

    #     # Показать график
    #     plotter.show()

    def make_3d_graph(self, x_coordinates, y_coordinates, z_coordinates, n_wells, file_type):
        # Нормализация координат Z
        z_min = np.min(z_coordinates)
        z_max = np.max(z_coordinates)
        z_range = z_max - z_min
        z_normalized = (z_coordinates - z_min) / z_range

        plotter = pv.Plotter()

        # Creating ground surface
        x_ground, y_ground = np.meshgrid(x_coordinates, y_coordinates)
        z_ground = np.zeros_like(x_ground)
        ground = pv.StructuredGrid(x_ground, y_ground, z_ground)
        plotter.add_mesh(ground, color="green", opacity=0.5, label="Ground")

        # Defining colors for wells
        colors = plt.cm.viridis(np.linspace(0, 1, n_wells))

        # Adding wells with different colors
        for i in range(n_wells):
            well_coordinates = np.column_stack((x_coordinates, y_coordinates, z_normalized[:, i]))
            well_polydata = pv.PolyData(well_coordinates)
            color = colors[i]
            plotter.add_mesh(well_polydata, color=color, point_size=10, render_points_as_spheres=True, label=f"Well {i+1}")

        # Adding legend with larger size
        plotter.add_legend(bcolor='black', face=None, size=(0.22, 0.22))

        # Adding text for min and max elevation
        min_elevation = np.min(z_coordinates)
        max_elevation = np.max(z_coordinates)
        plotter.add_text(f"Min Elevation: {min_elevation}", position="upper_left", font_size=12)
        plotter.add_text(f"Max Elevation: {max_elevation}", position="lower_left", font_size=12)

        # Show plot
        plotter.show()

