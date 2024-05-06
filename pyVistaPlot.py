import numpy as np
import pandas as pd
import pyvista as pv
import matplotlib.pyplot as plt
import itertools
from pyvista import examples

class Plot:
    def __init__(self, data_descriptor):
        self.data_descriptor = data_descriptor

    def load_file(self, file):
        data = pd.read_csv(file)


        self.data_descriptor._data = data

        return data

    def filter_data(self, data):
        well_data = self.data_descriptor._data

        n_wells = well_data.shape[1]
        x_coordinates = np.arange(n_wells)

        y_coordinates = np.arange(len(data))

        points = np.column_stack((np.repeat(x_coordinates, len(data)), np.tile(y_coordinates, n_wells), well_data.values.ravel()))

        # Reshape points to have shape (X, 3)
        points = points.reshape(-1, 3)

        return points, x_coordinates, y_coordinates, n_wells, well_data

    def make_3d_graph(self, points, x_coordinates, y_coordinates, n_weels, well_data, file_type):
        elevation_data = points[:, -1]

        print(f'ELEVATION DATA: {elevation_data}')

        point_cloud = pv.PolyData(points)
        point_cloud["elevation"] = elevation_data

        print(point_cloud)

        x_ground, y_ground = np.meshgrid(x_coordinates, y_coordinates)
        z_ground = np.zeros_like(x_ground)

        ground = pv.StructuredGrid(x_ground, y_ground, z_ground)

        plotter = pv.Plotter()
        plotter.add_mesh(ground, color="green", opacity=0.5, label="Ground")
        plotter.add_mesh(point_cloud, render_points_as_spheres=True, point_size=5, label="Point Cloud")

        print("WEELS: ", n_weels)
        for column_index in range(n_weels):
            column_points = well_data.iloc[:, column_index].values
            print(f' WEEL DATA: {well_data}')
            unique_points, point_counts = np.unique(column_points, return_counts=True)
            common_points = unique_points[point_counts > 1]

            for point_value in common_points:
                point_indices = np.where(column_points == point_value)[0] + column_index * len(y_coordinates)

                for i in range(len(point_indices) - 1):
                    line_points = np.array([points[point_indices[i]], points[point_indices[i + 1]]])
                    plotter.add_lines(line_points, color="blue", width=1)

        plotter.add_legend(bcolor='w', face=None)

        min_elevation = np.min(elevation_data)
        max_elevation = np.max(elevation_data)
        plotter.add_text(f"Min: {min_elevation}", position="upper_left", font_size=12)
        plotter.add_text(f"Max: {max_elevation}", position="lower_left", font_size=12)
        plotter.show()

