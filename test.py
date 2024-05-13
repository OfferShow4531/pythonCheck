# import numpy as np

# import pyvista as pv
# from pyvista import examples

# dem = examples.download_crater_topo()

# subset = dem.extract_subset((500, 900, 400, 800, 0, 0), (5, 5, 1))

# terrain = subset.warp_by_scalar()

# z_cells = np.array([25] * 5 + [35] * 3 + [50] * 2 + [75, 100])

# xx = np.repeat(terrain.x, len(z_cells), axis=-1)
# yy = np.repeat(terrain.y, len(z_cells), axis=-1)
# zz = np.repeat(terrain.z, len(z_cells), axis=-1) - np.cumsum(z_cells).reshape((1, 1, -1))

# mesh = pv.StructuredGrid(xx, yy, zz)
# mesh["Elevation"] = zz.ravel(order="F")


# cpos = [
#     (1826736.796308761, 5655837.275274233, 4676.8405505181745),
#     (1821066.1790519988, 5649248.765538796, 943.0995128226014),
#     (-0.2797856225380979, -0.27966946337594883, 0.9184252809434081),
# ]

# mesh.plot(show_edges=True, lighting=False, cpos=cpos)


import numpy as np
import pyvista as pv
from pyvista import examples

# Предоставленные данные
data = {
    'Timestamp': [1515974400, 1518652800, 1521072000, 1523750400, 1526342400],
    'Well1': [-6.33, -6.43, -6.44, -6.56, -6.60],
    'Well2': [-6.39, -6.40, -6.40, -6.42, -6.44],
    'Xpos': np.linspace(0, 10, 20),  # Увеличим количество точек вдоль оси X
    'Ypos': np.linspace(0, 10, 20)   # Увеличим количество точек вдоль оси Y
}

# Создаем сетку с использованием предоставленных данных
X, Y = np.meshgrid(data['Xpos'], data['Ypos'])

# Для z1 (Well1)
Z1 = np.repeat(np.repeat(data['Well1'], len(data['Xpos'])), len(data['Ypos'])).reshape(X.shape)

# Для z2 (Well2)
Z2 = np.repeat(np.repeat(data['Well2'], len(data['Xpos'])), len(data['Ypos'])).reshape(X.shape)

# Проверим размеры массивов
print("Shape of X:", X.shape)
print("Shape of Y:", Y.shape)
print("Shape of Z1:", Z1.shape)
print("Shape of Z2:", Z2.shape)

# Проверим снова размеры массивов
print("Shape of Z1 after correction:", Z1.shape)
print("Shape of Z2 after correction:", Z2.shape)

# Создаем структурированную сетку для z1
mesh1 = pv.StructuredGrid(X, Y, Z1)

# Создаем структурированную сетку для z2
mesh2 = pv.StructuredGrid(X, Y, Z2)

# Добавляем скалярные данные к сеткам из предоставленных данных
mesh1.point_data["Elevation"] = Z1.ravel(order="F")
mesh2.point_data["Elevation"] = Z2.ravel(order="F")

# Определяем dem, subset и terrain
dem = examples.download_crater_topo()
subset = dem.extract_subset((500, 900, 400, 800, 0, 0), (20, 20, 1))  # Увеличим количество точек вдоль оси X и Y
terrain = subset.warp_by_scalar()

# Создаем сетку на основе данных из terrain
mesh3 = pv.StructuredGrid(terrain.points)
mesh3.point_data["Elevation"] = terrain.points[:, 2]

# Объединяем все сетки
combined_mesh = mesh1 + mesh2 + mesh3

# Создаем график
plotter = pv.Plotter()

# Добавляем сетки на график
plotter.add_mesh(mesh1, color='blue', scalars="Elevation", show_scalar_bar=True)
plotter.add_mesh(mesh2, color='red', scalars="Elevation", show_scalar_bar=True)

# Отображаем график
plotter.show()