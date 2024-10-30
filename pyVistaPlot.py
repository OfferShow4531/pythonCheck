import pyvista as pv
import numpy as np
import time

class Plot:
    def __init__(self):
        self.plotter = pv.Plotter()

    def filter_data(self, data, timestamp):
        """Фильтрует данные по выбранному Timestamp."""
        timestamp_filtered = data[data['Timestamp'] == timestamp]

        if timestamp_filtered.empty:
            raise ValueError(f"Нет данных для timestamp {timestamp}.")

        # Извлечение координат X и Y (предполагаем, что они одинаковые для всех скважин)
        x_coordinate = timestamp_filtered['Xpos'].values[0]
        y_coordinate = timestamp_filtered['Ypos'].values[0]

        # Получение глубин для всех скважин (колонки Well1, Well2, ..., Well10)
        z_values = timestamp_filtered[['Well1', 'Well2', 'Well3', 'Well4', 'Well5',
                                       'Well6', 'Well7', 'Well8', 'Well9', 'Well10']].values

        # Транспонируем для удобства работы, чтобы каждая скважина была отдельной строкой
        z_coordinates = z_values.T
        n_wells = z_coordinates.shape[0]  # Количество скважин

        return x_coordinate, y_coordinate, z_coordinates, n_wells

    def make_3d_graph(self, x_coordinate, y_coordinate, z_coordinates, n_wells):
        """Создание 3D модели скважин с реалистичными почвенными слоями"""

        # Определение слоев почвы
        layers = [
            {'name': 'Organic', 'height': 2, 'color': 'brown', 'opacity': 0.9},
            {'name': 'Surface', 'height': 3, 'color': 'green', 'opacity': 0.5},
            {'name': 'Subsoil', 'height': 4, 'color': 'sandybrown', 'opacity': 0.7},
            {'name': 'Unconfined Aquifer', 'height': 5, 'color': 'lightblue', 'opacity': 0.6},
            {'name': 'Confined Layer', 'height': 4, 'color': 'gray', 'opacity': 0.9},
            {'name': 'Bedrock', 'height': 6, 'color': 'black', 'opacity': 0.9}
        ]

        current_depth = 0
        confined_layer_depth = 0  # Будет обновлено позже
        unconfined_layer_depth = 0  # Будет обновлено позже

        # Создаем и добавляем каждый слой почвы как объемный параллелепипед с вариацией в высоте поверхности
        for layer in layers:
            # Создание текстурированного верхнего слоя
            plane_resolution = 30  # Определяем разрешение плоскости (большее значение создаст больше точек)
            top_surface = pv.Plane(center=(0, 0, current_depth), i_size=60, j_size=60, i_resolution=plane_resolution, j_resolution=plane_resolution)

            # Генерация вариации высоты для каждого узла поверхности
            height_variation = np.random.uniform(-0.5, 0.5, top_surface.points.shape[0])
            top_surface.points[:, 2] += height_variation

            # Создание куба для слоя почвы
            bottom_z = current_depth - layer['height']
            cube = pv.Box(bounds=(-30, 30, -30, 30, bottom_z, current_depth))

            # Добавление слоя и верхней поверхности
            self.plotter.add_mesh(cube, color=layer['color'], opacity=layer['opacity'], label=layer['name'])
            self.plotter.add_mesh(top_surface, color=layer['color'], opacity=layer['opacity'] + 0.1)

            # Обновляем переменные глубины
            if layer['name'] == 'Confined Layer':
                confined_layer_depth = current_depth
            if layer['name'] == 'Unconfined Aquifer':
                unconfined_layer_depth = current_depth

            current_depth = bottom_z

        # Создаем смещение для каждой скважины, чтобы они не были в одной точке
        offsets = np.linspace(-25, 25, n_wells)  # Расширяем интервал между скважинами

        colors = ['blue', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'pink', 'brown', 'gray']

        for i in range(n_wells):
            z_value = z_coordinates[i][0]
            if np.isnan(z_value):
                print(f"Недостаточно данных для отображения скважины {i + 1}, пропуск.")
                continue

            # Ограничиваем глубину скважин уровнем между confined и unconfined aquifer слоями
            self.create_well(
                x_coordinate + offsets[i], y_coordinate, confined_layer_depth, colors[i % len(colors)]
            )

        self.add_legend(colors)

        # Показ модели и запуск анимации дождя и инфильтрации
        self.plotter.show(interactive=True)

    def create_well(self, x, y, confined_depth, color):
        """Создает визуализацию скважины как цилиндр, пронизывающий верхние слои, но не ниже confined слоя"""
        # Высота скважины должна доходить до верхнего слоя и не заходить глубже ограниченного слоя (confined layer)
        well_height = abs(confined_depth)

        # Создаем цилиндр для скважины, направленный вниз от поверхности
        well_cylinder = pv.Cylinder(center=(x, y, confined_depth / 2), radius=0.5, height=well_height, direction=(0, 0, -1))
        self.plotter.add_mesh(well_cylinder, color=color, opacity=0.9, label=f'Well {color}')

    def add_legend(self, colors):
        """Добавляет легенду на график"""
        legend_labels = [
            ("Organic", "brown"),
            ("Surface", "green"),
            ("Subsoil", "sandybrown"),
            ("Unconfined Aquifer", "lightblue"),
            ("Confined Layer", "gray"),
            ("Bedrock", "black")
        ]
        legend_labels += [(f"Well ({color})", color) for color in colors]

        self.plotter.add_text("Well", position="upper_right", font_size=10, color="blue")
        self.plotter.add_legend(labels=legend_labels, bcolor="white")

    def animate_rain_infiltration(self, unconfined_layer_depth):
        """Создает анимацию дождя и инфильтрации воды на уровне Unconfined Aquifer"""
        num_drops = 50  # Количество капель дождя
        drop_radius = 0.3  # Радиус капли
        rain_duration = 5  # Продолжительность дождя (в секундах)

        # Генерация случайных позиций для капель дождя
        x_positions = np.random.uniform(-25, 25, num_drops)
        y_positions = np.random.uniform(-25, 25, num_drops)
        initial_height = 10  # Высота, с которой начинается падение капель

        # Добавление капель и анимация их падения
        rain_drops = []
        for i in range(num_drops):
            rain_drop = pv.Sphere(center=(x_positions[i], y_positions[i], initial_height), radius=drop_radius)
            rain_actor = self.plotter.add_mesh(rain_drop, color='blue', opacity=0.5)
            rain_drops.append((rain_drop, rain_actor))

        # Анимация движения капель вниз
        num_steps = 30  # Количество шагов анимации
        for step in range(num_steps):
            for rain_drop, rain_actor in rain_drops:
                new_z = rain_drop.center[2] - (initial_height - unconfined_layer_depth) / num_steps
                rain_drop.translate((0, 0, -new_z), inplace=True)
                self.plotter.update_coordinates(rain_drop.points, render=False)
            time.sleep(rain_duration / num_steps)
            self.plotter.render()  # Обновление сцены для визуализации анимации

    def save_current_model(self, filename="well_model.png"):
        """Сохраняет текущую модель в файл"""
        if self.plotter:
            self.plotter.screenshot(filename)
            print(f"Модель успешно сохранена как {filename}")