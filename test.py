import pandas as pd
import pyvista as pv

# Пример данных
data = {
    "Timestamp": [1515974400, 1518652800, 1521072000, 1523750400, 1526342400],
    "Well1": [-6.33, -6.43, -6.44, -6.56, -6.6],
    "Well2": [-6.39, -6.4, -6.4, -6.42, -6.44],
    "Well3": [-7.27, -7.32, -7.3, -7.45, -7.5],
    "Well4": [-7.14, -7.16, -7.14, -7.17, -7.17],
    "Well5": [-7.15, -7.2, -7.19, -7.32, -7.38],
    "Well6": [-7.14, -7.16, -7.15, -7.17, -7.17],
    "Well7": [-6.68, -6.7, -6.71, -6.7, -6.6],
    "Well8": [-6.31, -6.32, -6.33, -6.34, -6.35],
    "Well9": [-5.65, -5.8, -5.88, -5.9, -5.9],
    "Well10": [-5.79, -5.81, -5.83, -5.86, -5.88],
    "Xpos": [0, 0, 0, 0, 0],
    "Ypos": [0, 1, 2, 3, 4],
}

# Преобразуем данные в DataFrame
df = pd.DataFrame(data)

# Метод для рисования скважины с почвой
def draw_well_with_soil(df):
    # Создаем объект визуализации
    plotter = pv.Plotter()

    # Получаем координаты X и Y
    xpos = df['Xpos'].iloc[0]
    ypos = df['Ypos'].iloc[0]

    # Создаем вертикальный цилиндр для скважины
    well_height = -df['Well1'].mean()  # Пример высоты скважины
    well_radius = 0.1  # Радиус скважины
    well_cylinder = pv.Cylinder(center=(xpos, ypos, 0), radius=well_radius, height=well_height)

    # Добавляем цилиндр скважины на график
    plotter.add_mesh(well_cylinder, color='blue', opacity=0.7, label='Well')

    # Создаем слои почвы
    soil_depths = [-5, -5.5, -6, -6.5, -7, -7.5]  # Пример глубин почвы
    soil_types = ['Top Soil', 'Clay', 'Silt', 'Sand', 'Gravel']  # Типы почвы
    colors = ['#D2B48C', '#8B4513', '#C0C0C0', '#DEB887', '#A0522D']  # Цвета для каждого слоя

    for i, (depth, soil_type) in enumerate(zip(soil_depths, soil_types)):
        # Создаем горизонтальную плоскость почвы
        soil_plane = pv.Plane(i_size=1, j_size=1, i_resolution=10, j_resolution=10)
        soil_plane.rotate_x(90)  # Поворачиваем плоскость
        soil_plane.translate((xpos, ypos, depth))  # Перемещаем на нужную глубину

        # Добавляем плоскость почвы на график
        plotter.add_mesh(soil_plane, color=colors[i], opacity=0.5, label=soil_type)

    # Настройка визуализации
    plotter.add_legend()
    plotter.set_background('white')
    plotter.show_grid()

    # Отображение графика
    plotter.show()

# Вызов метода
draw_well_with_soil(df)