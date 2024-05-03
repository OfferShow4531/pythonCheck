import numpy as np

import pandas as pd
import pyvista as pv
import itertools
from pyvista import examples

# def generate_points(subset=0.02):
#     """A helper to make a 3D NumPy array of points (n_points by 3)"""
#     dataset = examples.download_lidar()
#     ids = np.random.randint(low=0, high=dataset.n_points - 1, size=int(dataset.n_points * subset))
#     return dataset.points[ids]


# points = generate_points()
# # Print first 5 rows to prove its a numpy array (n_points by 3)
# # Columns are (X Y Z)
# points[0:5, :]

# point_cloud = pv.PolyData(points)
# np.allclose(points, point_cloud.points)

# # point_cloud.plot(eye_dome_lighting=True)


# # Make data array using z-component of points array
# data = points[:, -1]

# # Add that data to the mesh with the name "uniform dist"
# point_cloud["elevation"] = data


# point_cloud.plot(render_points_as_spheres=True)

# Load the data from CSV
data = pd.read_csv('timeseries/multipledata.csv')

# Extracting well data
well_data = data.drop(columns=['timeStamp']).values

# Creating X-coordinates for the wells
n_wells = well_data.shape[1]  # Number of wells
x_coordinates = np.arange(n_wells)

# Creating Y-coordinates for the measurements (using timestamps as Y-coordinates)
y_coordinates = np.arange(len(data))

# Creating the grid of points
points = np.column_stack((np.repeat(x_coordinates, len(data)), np.tile(y_coordinates, n_wells), well_data.ravel()))

# Reshape points to have shape (X, 3)
points = points.reshape(-1, 3)

# Make data array using z-component of points array
elevation_data = points[:, -1]

# Add that data to the mesh with the name "elevation"
point_cloud = pv.PolyData(points)
point_cloud["elevation"] = elevation_data

# Creating a grid representing the ground
x_ground, y_ground = np.meshgrid(x_coordinates, y_coordinates)
z_ground = np.zeros_like(x_ground)  # Setting the ground level to zero

# Create a StructuredGrid representing the ground
ground = pv.StructuredGrid(x_ground, y_ground, z_ground)

# Displaying the point cloud and the ground
plotter = pv.Plotter()
plotter.add_mesh(ground, color="green", opacity=0.5)  # Adding the ground with opacity
plotter.add_mesh(point_cloud, render_points_as_spheres=True)  # Adding the point cloud

# Create combinations of pairs of elements
element_pairs = list(itertools.combinations(range(n_wells), 2))

# Create a list to store all common points
all_common_points = []

# Loop through each pair and find common points
for pair in element_pairs:
    element1_index, element2_index = pair
    
    # Find common points between element1 and element2
    common_points = []  # List to store common points between the pair
    for i, point1 in enumerate(well_data[:, element1_index]):
        for j, point2 in enumerate(well_data[:, element2_index]):
            if point1 == point2:
                common_points.append((i, j))
    
    print(common_points)
    
    # Append common points to the list of all common points
    all_common_points.extend(common_points)

# Создание линий между общими точками
for p1, p2 in common_points:
    line_points = np.array([points[p1], points[p2]])
    plotter.add_lines(line_points, color="blue", width=1)

plotter.show()