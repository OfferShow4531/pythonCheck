import numpy as np

import pandas as pd
import pyvista as pv
import itertools
from pyvista import examples

class Plot:
    def __init__(self, data_descriptor):
        self.data_descriptor = data_descriptor

    def load_file(self, file):
        # Загрузка данных из CSV
        data = pd.read_csv(file)

        # Устанавливаем данные в дескриптор
        self.data_descriptor._data = data

        # Используем дескриптор для фильтрации данных
        return data

    def filter_data(self, data):
        # Используем дескриптор для фильтрации данных
        weel_data = self.data_descriptor._data

        # Создаем X-координаты для скважин
        n_wells = weel_data.shape[1]  # Количество скважин
        x_coordinates = np.arange(n_wells)

        # Создаем Y-координаты для измерений (используем временные метки как Y-координаты)
        y_coordinates = np.arange(len(data))

        # Создаем сетку точек
        points = np.column_stack((np.repeat(x_coordinates, len(data)), np.tile(y_coordinates, n_wells), weel_data.values.ravel()))

        # Reshape points to have shape (X, 3)
        points = points.reshape(-1, 3)

        return points, x_coordinates, y_coordinates, n_wells, weel_data

    def make_3d_graph(self, points, x_coordinates, y_coordinates, n_weels, weel_data):
       # Make data array using z-component of points array
        elevation_data = points[:, -1]

        print(f'ELEVATION DATA: {elevation_data}')

        # Add that data to the mesh with the name "elevation"
        point_cloud = pv.PolyData(points)
        point_cloud["elevation"] = elevation_data

        print(point_cloud)

        # Creating a grid representing the ground
        x_ground, y_ground = np.meshgrid(x_coordinates, y_coordinates)
        z_ground = np.zeros_like(x_ground)  # Setting the ground level to zero

        # Create a StructuredGrid representing the ground
        ground = pv.StructuredGrid(x_ground, y_ground, z_ground)

        # Displaying the point cloud and the ground
        plotter = pv.Plotter()
        plotter.add_mesh(ground, color="green", opacity=0.5, label="Ground")  # Adding the ground with opacity
        plotter.add_mesh(point_cloud, render_points_as_spheres=True, point_size=5, label="Point Cloud")  # Adding the point cloud

        print("WEELS: ", n_weels)
        # Создание линий между общими точками
        for column_index in range(n_weels):
            # Find common points within the current column
            column_points = weel_data.iloc[:, column_index].values
            print(f' WEEL DATA: {weel_data}')
            unique_points, point_counts = np.unique(column_points, return_counts=True)
            common_points = unique_points[point_counts > 1]  # Select points that appear more than once

            # Создание линий между всеми общими точками внутри столбца
            for point_value in common_points:
                # Получаем индексы точек в массиве points
                point_indices = np.where(column_points == point_value)[0] + column_index * len(y_coordinates)

                # Создаем линии между парами общих точек внутри столбца
                for i in range(len(point_indices) - 1):
                    line_points = np.array([points[point_indices[i]], points[point_indices[i + 1]]])
                    plotter.add_lines(line_points, color="blue", width=1)

        plotter.add_legend(bcolor='w', face=None)

        min_elevation = np.min(elevation_data)
        max_elevation = np.max(elevation_data)
        plotter.add_text(f"Min: {min_elevation}", position="upper_left", font_size=12)
        plotter.add_text(f"Max: {max_elevation}", position="lower_left", font_size=12)

        plotter.show()
