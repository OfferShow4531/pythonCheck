import numpy as np
import pyvista as pv
import logging
from tkinter import filedialog, messagebox

# Устанавливаем настройки логирования
logging.basicConfig(filename='error.log', level=logging.DEBUG)

class Plot:
    def __init__(self):
        self.plotter = None

    def filter_data(self, data, timestamp):
        """Фильтрует данные по выбранному Timestamp"""
        timestamp_filtered = data[data['Timestamp'] == timestamp]
        if timestamp_filtered.empty:
            return None

        x_coordinates = timestamp_filtered['Xpos'].values
        y_coordinates = timestamp_filtered['Ypos'].values
        z_coordinates = timestamp_filtered.drop(columns=['Timestamp', 'Xpos', 'Ypos']).values.T
        n_wells = z_coordinates.shape[0]
        return x_coordinates, y_coordinates, z_coordinates, n_wells

    def make_3d_graph(self, x_coordinates, y_coordinates, z_coordinates, n_wells):
        """Создание 3D модели скважин"""
        self.plotter = pv.Plotter()
        
        if len(x_coordinates) == 0 or len(y_coordinates) == 0 or len(z_coordinates) == 0:
            print("Нет данных для отрисовки скважин.")
            return

        print(f"X Coordinates: {x_coordinates}")
        print(f"Y Coordinates: {y_coordinates}")
        print(f"Z Coordinates:\n{z_coordinates}")
        print(f"Number of Wells: {n_wells}")


        colors = ['brown', 'gray', 'blue', 'green', 'yellow']

        # Реалистичная земля с возвышенностями
        terrain_size = 10  # Размер участка земли
        terrain_height = 5  # Высота рельефа
        terrain = pv.Plane(i_size=terrain_size, j_size=terrain_size)
        noise = np.random.normal(0, 1, size=(terrain.points.shape[0],))
        terrain.points[:, 2] = noise * terrain_height  # Неровная земля

        self.plotter.add_mesh(terrain, color="green", opacity=0.7)

        # Создание слоев почвы и пород
        self.add_soil_layers(terrain_size)

        # Используем общие координаты для всех скважин
        x = x_coordinates[0]  # Используем первую координату X
        y = y_coordinates[0]  # Используем первую координату Y

        for i in range(n_wells):
            if i < len(z_coordinates):
                z_min = z_coordinates[i][0]  # Нижняя точка скважины
                z_max = z_min # Если одна точка, то z_max = z_min
                height = 1  # Высота цилиндра для визуализации
                print(f"Well {i + 1}: X={x}, Y={y}, Z_min={z_min}, Z_max={z_max}, Height={height}")

                cylinder = pv.Cylinder(center=(x, y, z_min + height / 2), direction=(0, 0, 1), radius=0.2, height=height)
                color = self.get_color_by_well(i)  # Разные цвета для разных скважин
                self.plotter.add_mesh(cylinder, color=color, opacity=0.9)
            else:
                print(f"Не хватает данных для скважины {i + 1}")

        # Добавляем легенду с n_wells
        self.add_legend(colors, n_wells)

        self.plotter.show()

    def add_soil_layers(self, terrain_size):
        """Добавление слоев почвы и пород"""
        soil_thickness = 5
        rock_thickness = 5
        gravel_thickness = 5
        bedrock_thickness = 5

        # Плодородная почва (толщина 5 метров)
        soil = pv.Cube(center=(0, 0, -soil_thickness / 2), x_length=terrain_size, y_length=terrain_size, z_length=soil_thickness)
        self.plotter.add_mesh(soil, color="brown", opacity=0.8)

        # Каменная порода
        rock = pv.Cube(center=(0, 0, -(soil_thickness + rock_thickness / 2)), x_length=terrain_size, y_length=terrain_size, z_length=rock_thickness)
        self.plotter.add_mesh(rock, color="gray", opacity=0.8)

        # Гравий
        gravel = pv.Cube(center=(0, 0, -(soil_thickness + rock_thickness + gravel_thickness / 2)), x_length=terrain_size, y_length=terrain_size, z_length=gravel_thickness)
        self.plotter.add_mesh(gravel, color="darkgray", opacity=0.7)

        # Бедрок
        bedrock = pv.Cube(center=(0, 0, -(soil_thickness + rock_thickness + gravel_thickness + bedrock_thickness / 2)), x_length=terrain_size, y_length=terrain_size, z_length=bedrock_thickness)
        self.plotter.add_mesh(bedrock, color="black", opacity=0.9)

        # Модель подземных вод (например, под гравием)
        water_thickness = 3
        water = pv.Cube(center=(0, 0, -(soil_thickness + rock_thickness + water_thickness / 2)), x_length=terrain_size, y_length=terrain_size, z_length=water_thickness)
        self.plotter.add_mesh(water, color="cyan", opacity=0.5)

    def get_color_by_well(self, index):
        """Возвращает цвет для каждой скважины на основе ее индекса"""
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan", "magenta", "brown"]
        return colors[index % len(colors)]

    def add_legend(self, colors, n_wells):
        """Добавление легенды для скважин"""
        # Создаем отдельный контейнер для легенды
        self.plotter.add_text(f"Количество скважин: {n_wells}", position='upper_right', font_size=10)
        self.plotter.add_text("Скважины", position='upper_left', font_size=12)

        for i, color in enumerate(colors):
            legend_sphere = pv.Sphere(radius=0.1, center=(0.5, 0.5, 0))  # Используем сферы как маркеры
            self.plotter.add_mesh(legend_sphere, color=color, opacity=1)
            self.plotter.add_text(f"Скважина {i + 1}", position='upper_left', font_size=10)

    def add_landscape_legend(self):
        """Добавление легенды для ландшафта"""
        self.plotter.add_text("Ландшафт:", position='upper_right', font_size=12)

        # Добавляем описание для каждого слоя
        self.plotter.add_text("Коричневый: Плодородная почва", position='upper_right', font_size=10)
        self.plotter.add_text("Серый: Каменная порода", position='upper_right', font_size=10)
        self.plotter.add_text("Темно-серый: Гравий", position='upper_right', font_size=10)
        self.plotter.add_text("Черный: Бедрок", position='upper_right', font_size=10)
        self.plotter.add_text("Голубой: Подземные воды", position='upper_right', font_size=10)

    def save_current_model(self):
        """Сохранение текущей модели в файл"""
        file_path = filedialog.asksaveasfilename(defaultextension=".vtk", filetypes=[("VTK files", "*.vtk")])
        if file_path:
            self.plotter.save(file_path)
            messagebox.showinfo("Сохранение", "Модель успешно сохранена.")