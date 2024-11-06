import pyvista as pv #PyVista
import numpy as np
import random

class Plot:
    def __init__(self):
        self.plotter = pv.Plotter()
        self.layers = [
            {'name': 'Organic', 'height': 2, 'color': 'brown', 'opacity': 0.9},
            {'name': 'Surface', 'height': 3, 'color': 'green', 'opacity': 0.5},
            {'name': 'Subsoil', 'height': 4, 'color': 'sandybrown', 'opacity': 0.7},
            {'name': 'Unconfined Aquifer', 'height': 5, 'color': 'lightblue', 'opacity': 0.6},
            {'name': 'Confined Layer', 'height': 4, 'color': 'gray', 'opacity': 0.9},
            {'name': 'Bedrock', 'height': 6, 'color': 'black', 'opacity': 0.9}
        ]
        self.num_drops = 10  # Количество капель дождя
        self.steps = 120     # Количество шагов анимации
        self.puddles = {}    # Словарь для хранения луж и их размеров
        self.soil_meshes = []  # Список для хранения объектов слоев почвы
        self.temp_actors = []  # Список для временных объектов анимации дождя

    def filter_data(self, data, timestamp):
        timestamp_filtered = data[data['Timestamp'] == timestamp]

        if timestamp_filtered.empty:
            raise ValueError(f"Нет данных для timestamp {timestamp}.")

        x_coordinate = timestamp_filtered['Xpos'].values[0]
        y_coordinate = timestamp_filtered['Ypos'].values[0]
        z_values = timestamp_filtered[['Well1', 'Well2', 'Well3', 'Well4', 'Well5',
                                       'Well6', 'Well7', 'Well8', 'Well9', 'Well10']].values
        z_coordinates = z_values.T
        n_wells = z_coordinates.shape[0]

        return x_coordinate, y_coordinate, z_coordinates, n_wells

    def draw_static_soil_layers(self):
        """Отрисовка слоев почвы один раз и сохранение объектов в self.soil_meshes"""
        current_depth = 0
        for layer in self.layers:
            plane_resolution = 30
            top_surface = pv.Plane(center=(0, 0, current_depth), i_size=60, j_size=60, i_resolution=plane_resolution, j_resolution=plane_resolution)
            height_variation = np.random.uniform(-0.5, 0.5, top_surface.points.shape[0])
            top_surface.points[:, 2] += height_variation

            bottom_z = current_depth - layer['height']
            cube = pv.Box(bounds=(-30, 30, -30, 30, bottom_z, current_depth))
            soil_mesh_cube = self.plotter.add_mesh(cube, color=layer['color'], opacity=layer['opacity'], label=layer['name'])
            soil_mesh_top = self.plotter.add_mesh(top_surface, color=layer['color'], opacity=layer['opacity'] + 0.1)

            # Добавляем объекты почвы в список, чтобы они не были удалены в процессе анимации
            self.soil_meshes.append(soil_mesh_cube)
            self.soil_meshes.append(soil_mesh_top)

            current_depth = bottom_z

    def make_3d_graph(self, x_coordinate, y_coordinate, z_coordinates, n_wells):
        """Создание 3D модели скважин с реалистичными почвенными слоями и анимацией дождя"""
        self.draw_static_soil_layers()
        self.create_wells(x_coordinate, y_coordinate, z_coordinates, n_wells)

        # Запуск анимации дождя и инфильтрации после создания 3D-модели
        self.plotter.open_gif("rain_with_puddles_and_streams.gif")
        self.animate_rain()
        self.plotter.close()  # Закрываем GIF после завершения анимации

        # Показ модели
        self.plotter.show(interactive=True)

    def create_wells(self, x_coordinate, y_coordinate, z_coordinates, n_wells):
        """Создание визуализации скважин"""
        # Создаем смещение для каждой скважины, чтобы они не были в одной точке
        offsets = np.linspace(-25, 25, n_wells)
        colors = ['blue', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'pink', 'brown', 'gray']

        for i in range(n_wells):
            z_value = z_coordinates[i][0]
            if np.isnan(z_value):
                print(f"Недостаточно данных для отображения скважины {i + 1}, пропуск.")
                continue
            self.create_well(x_coordinate + offsets[i], y_coordinate, -15, colors[i % len(colors)])  # Используем -15 для ограниченного слоя

    def create_well(self, x, y, confined_depth, color):
        well_height = abs(confined_depth)
        well_cylinder = pv.Cylinder(center=(x, y, confined_depth / 2), radius=0.5, height=well_height, direction=(0, 0, -1))
        self.plotter.add_mesh(well_cylinder, color=color, opacity=0.9, label=f'Well {color}')

    def add_legend(self, colors):
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

    def create_zigzag_stream(self, start, length=1.0, amplitude=0.2):
        x_values = np.linspace(start[0], start[0], 10)
        y_values = np.linspace(start[1], start[1], 10)
        z_values = np.linspace(start[2], start[2] - length, 10)
        for i in range(1, len(z_values) - 1):
            x_values[i] += np.random.uniform(-amplitude, amplitude)
            y_values[i] += np.random.uniform(-amplitude, amplitude)
        return x_values, y_values, z_values

    # REWORKED GIT BLAME VLADIMIR
    def animate_rain(self):
        """Основной метод анимации дождя и инфильтрации."""
        # Инициализация капель дождя
        drops = self.initialize_drops()
        # Начальная глубина инфильтрации
        infiltration_depth = self.layers[0]['height']
        # Настройка начальных объектов капель дождя
        drop_actors, drop_meshes = self.setup_drop_meshes(drops)

        for step in range(self.steps):
            self.update_raindrops(drops, drop_meshes)  # Обновление позиций капель
            self.update_puddles(drops)  # Обновление или создание луж
            self.visualize_infiltration(infiltration_depth)  # Визуализация инфильтрации
            infiltration_depth -= 0.1  # Увеличение глубины инфильтрации
            self.plotter.write_frame()  # Запись текущего кадра в GIF

        # Чтобы не останавливалось
        self.plotter.show(interactive=True)

    def initialize_drops(self):
        """Создает начальные позиции для капель дождя."""
        return [
            {'position': [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(5, 15)], 'is_stream': False}
            for _ in range(self.num_drops)]

    def setup_drop_meshes(self, drops):
        """Создает и добавляет объекты капель дождя в сцену, возвращает списки капель и их объектов."""
        drop_meshes = [pv.Sphere(radius=0.1, center=drop['position']) for drop in drops]
        drop_actors = [self.plotter.add_mesh(mesh, color='lightblue') for mesh in drop_meshes]
        return drop_actors, drop_meshes

    def update_raindrops(self, drops, drop_meshes):
        """Обновляет позиции капель дождя, создает потоки если достигнут уровень луж."""
        for i, drop in enumerate(drops):
            x, y, z = drop['position']
            z -= 0.2  # Капля падает каждый шаг
            if drop['is_stream']:
                self.create_stream(drop, x, y, z)
            else:
                drop_meshes[i].points = pv.Sphere(radius=0.1, center=(x, y, z)).points
            drop['position'] = [x, y, z]

    # REWORKED GIT BLAME VLADIMIR
    def create_stream(self, drop, x, y, z):
        """Создает и визуализирует поток из капли дождя с расширяющимся эффектом."""
        x_values, y_values, z_values = self.create_zigzag_stream((x, y, z), length=3,
                                                                 amplitude=0.4)  # Увеличенная амплитуда для большего отклонения
        branch_step = 5  # Большой шаг для снижения количества фрагментов

        for j in range(0, len(z_values) - branch_step, branch_step):
            # Начальные и конечные точки сегмента потока
            pointa = (x_values[j], y_values[j], z_values[j])
            pointb = (x_values[j + branch_step] + np.random.uniform(-0.3, 0.3),
                      y_values[j + branch_step] + np.random.uniform(-0.3, 0.3),
                      z_values[j + branch_step])

            # Создаем основной сегмент потока с уменьшенной шириной
            line_segment = pv.Line(pointa=pointa, pointb=pointb)
            self.plotter.add_mesh(line_segment, color='lightblue', line_width=2)  # Более тонкая линия

            # Добавляем боковые "ветви" с увеличенным смещением
            branch_offset = np.random.uniform(-0.8, 0.8)  # Значительное смещение для расширяющегося эффекта
            branch_a = pv.Line(pointa=pointa, pointb=(pointb[0] + branch_offset, pointb[1], pointb[2] - 0.1))
            branch_b = pv.Line(pointa=pointa, pointb=(pointb[0] - branch_offset, pointb[1], pointb[2] - 0.1))

            # Визуализация тонких "ветвей"
            self.plotter.add_mesh(branch_a, color='lightblue', line_width=1)
            self.plotter.add_mesh(branch_b, color='lightblue', line_width=1)

            # Когда поток достигает уровня -20, направляем его в стороны
            if pointb[2] <= -15:
                lateral_offset = np.random.uniform(0.5, 10.0)  # Боковое расширение на нижнем уровне
                lateral_a = pv.Line(pointa=pointb, pointb=(pointb[0] + lateral_offset, pointb[1], pointb[2]))
                lateral_b = pv.Line(pointa=pointb, pointb=(pointb[0] - lateral_offset, pointb[1], pointb[2]))
                self.plotter.add_mesh(lateral_a, color='lightblue', line_width=1)
                self.plotter.add_mesh(lateral_b, color='lightblue', line_width=1)

        # Завершение потока
        if z <= -20:
            drop['is_stream'] = False

    def update_puddles(self, drops):
        """Создает и увеличивает лужи на поверхности при достижении каплями нужного уровня."""
        for drop in drops:
            if not drop['is_stream'] and drop['position'][2] <= -5:
                drop['is_stream'] = True
                x, y = round(drop['position'][0]), round(drop['position'][1])
                puddle_key = (x, y)
                if puddle_key in self.puddles:
                    self.puddles[puddle_key] += 0.1
                    self.update_puddle(puddle_key)
                else:
                    self.create_puddle(puddle_key)

    def create_puddle(self, puddle_key):
        """Создает новую лужу на поверхности."""
        x, y = puddle_key
        self.puddles[puddle_key] = 0.3
        puddle = pv.Disc(center=(x, y, 0), inner=0, outer=self.puddles[puddle_key], normal=(0, 0, 1))
        self.plotter.add_mesh(puddle, color="lightblue", opacity=0.6)

    def update_puddle(self, puddle_key):
        """Обновляет существующую лужу, увеличивая её размер."""
        puddle_discs = self.puddles[puddle_key]
        puddle_discs.scale(self.puddles[puddle_key])

    def visualize_infiltration(self, infiltration_depth):
        """Создает и визуализирует уровень инфильтрации под лужами."""
        for (px, py), size in self.puddles.items():
            infiltration = pv.Disc(center=(px, py, infiltration_depth), inner=0, outer=size + 0.2, normal=(0, 0, 1))
            self.plotter.add_mesh(infiltration, color="lightblue", opacity=0.3)