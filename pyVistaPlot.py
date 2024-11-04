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

        # Отрисовываем слои почвы один раз
        if not self.soil_meshes:  # Если слои почвы еще не отрисованы
            self.draw_static_soil_layers()

        # Создаем смещение для каждой скважины, чтобы они не были в одной точке
        offsets = np.linspace(-25, 25, n_wells)
        colors = ['blue', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'pink', 'brown', 'gray']

        for i in range(n_wells):
            z_value = z_coordinates[i][0]
            if np.isnan(z_value):
                print(f"Недостаточно данных для отображения скважины {i + 1}, пропуск.")
                continue

            # Ограничиваем глубину скважин уровнем между confined и unconfined aquifer слоями
            self.create_well(x_coordinate + offsets[i], y_coordinate, -15, colors[i % len(colors)])  # Используем -15 для ограниченного слоя

        self.add_legend(colors)

        # Запуск анимации дождя и инфильтрации после создания 3D-модели
        self.plotter.open_gif("rain_with_puddles_and_streams.gif")
        self.animate_rain()
        self.plotter.close()  # Закрываем GIF после завершения анимации

        # Показ модели
        self.plotter.show(interactive=True)

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

    def animate_rain(self):
        """Анимация дождя с эффектом инфильтрации, начиная с уровня Organic"""

        # Начальные позиции капель дождя
        drops = [{'position': [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(5, 15)], 'is_stream': False} for _ in range(self.num_drops)]
        
        # Устанавливаем начальную глубину инфильтрации на нижней границе слоя Organic
        organic_layer_depth = -self.layers[0]['height']  # Глубина нижней границы слоя Organic
        infiltration_depth = organic_layer_depth  # Начинаем инфильтрацию на уровне Organic

        # Инициализация объектов дождевых капель и луж
        drop_meshes = [pv.Sphere(radius=0.1, center=drop['position']) for drop in drops]
        drop_actors = [self.plotter.add_mesh(mesh, color='lightblue') for mesh in drop_meshes] # Отрисовка луж
        puddle_discs = {}

        for step in range(self.steps):
            # Обновляем позиции дождевых капель
            for i, drop in enumerate(drops):
                x, y, z = drop['position']
                z -= 0.2  # Капля падает каждый шаг

                # Если капля достигла уровня луж, создаем или увеличиваем лужу
                if z <= -5 and not drop['is_stream']:
                    drop['is_stream'] = True
                    puddle_key = (round(x), round(y))

                    # Создаем или увеличиваем лужу на этой позиции
                    if puddle_key in self.puddles:
                        self.puddles[puddle_key] += 0.1  # Увеличиваем размер лужи
                        # Обновляем существующую лужу
                        puddle_discs[puddle_key].points[:, 2] = -5  # Установка на поверхность
                        puddle_discs[puddle_key].scale(self.puddles[puddle_key])
                    else:
                        self.puddles[puddle_key] = 0.3   # Начальный размер новой лужи
                        # Добавляем новую лужу
                        puddle = pv.Disc(center=(x, y, -5), inner=0, outer=self.puddles[puddle_key], normal=(0, 0, 1))
                        puddle_discs[puddle_key] = self.plotter.add_mesh(puddle, color="lightblue", opacity=0.6)
                    continue

                # Если капля в режиме "струи", обновляем её положение, чтобы создавать зигзагообразный поток вниз
                if drop['is_stream']:
                    x_values, y_values, z_values = self.create_zigzag_stream((x, y, z), length=5)

                    # Рисуем каждый сегмент потока и сохраняем акторы
                    for j in range(len(z_values) - 1):
                        line_segment = pv.Line(pointa=(x_values[j], y_values[j], z_values[j]),
                                            pointb=(x_values[j + 1], y_values[j + 1], z_values[j + 1]))
                        self.plotter.add_mesh(line_segment, color='lightblue', line_width=3)
                    
                    if z <= -20:
                        drop['is_stream'] = False

                # Обновляем положение капли, изменяя точки сфер
                drop_meshes[i].points = pv.Sphere(radius=0.1, center=(x, y, z)).points
                # Обновляем положение капли
                drop['position'] = [x, y, z]

            # Визуализация инфильтрации под лужами, начиная с уровня Organic и постепенно опускаясь
            for (px, py), size in self.puddles.items():
                infiltration = pv.Disc(center=(px, py, infiltration_depth), inner=0, outer=size + 0.2, normal=(0, 0, 1))
                self.plotter.add_mesh(infiltration, color="lightblue", opacity=0.3)

            # Увеличиваем глубину инфильтрации для следующего кадра
            infiltration_depth -= 0.1

            # Запись текущего кадра в GIF
            self.plotter.write_frame()