import pyvista as pv
import numpy as np
import time
import random

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
            plane_resolution = 30
            top_surface = pv.Plane(center=(0, 0, current_depth), i_size=60, j_size=60, i_resolution=plane_resolution, j_resolution=plane_resolution)
            height_variation = np.random.uniform(-0.5, 0.5, top_surface.points.shape[0])
            top_surface.points[:, 2] += height_variation

            bottom_z = current_depth - layer['height']
            cube = pv.Box(bounds=(-30, 30, -30, 30, bottom_z, current_depth))

            self.plotter.add_mesh(cube, color=layer['color'], opacity=layer['opacity'], label=layer['name'])
            self.plotter.add_mesh(top_surface, color=layer['color'], opacity=layer['opacity'] + 0.1)

            if layer['name'] == 'Confined Layer':
                confined_layer_depth = current_depth
            if layer['name'] == 'Unconfined Aquifer':
                unconfined_layer_depth = current_depth

            current_depth = bottom_z

        offsets = np.linspace(-25, 25, n_wells)
        colors = ['blue', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'pink', 'brown', 'gray']

        for i in range(n_wells):
            z_value = z_coordinates[i][0]
            if np.isnan(z_value):
                print(f"Недостаточно данных для отображения скважины {i + 1}, пропуск.")
                continue

            self.create_well(
                x_coordinate + offsets[i], y_coordinate, confined_layer_depth, colors[i % len(colors)]
            )

        self.add_legend(colors)
        self.plotter.show(interactive=True)

    def create_well(self, x, y, confined_depth, color):
        """Создает визуализацию скважины как цилиндр, пронизывающий верхние слои, но не ниже confined слоя"""
        well_height = abs(confined_depth)
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

    def create_short_zigzag(self, start, direction, length=1.0, amplitude=0.2):
        """Создаёт короткую зигзагообразную линию для струи."""
        x_values = np.linspace(start[0], start[0] + direction[0] * length, 4)
        y_values = np.linspace(start[1], start[1] + direction[1] * length, 4)
        z_values = np.linspace(start[2], start[2] + direction[2] * length, 4)

        for i in range(1, len(x_values) - 1):
            x_values[i] += amplitude * np.random.uniform(-0.5, 0.5)
            y_values[i] += amplitude * np.random.uniform(-0.5, 0.5)

        return x_values, y_values, z_values

    def animate_rain_infiltration(self, unconfined_layer_depth, confined_layer_depth):
        """Создает анимацию дождя с образованием луж и зигзагообразных струй до четвертого слоя и сохраняет в GIF."""
        num_drops = 50
        drop_radius = 0.3
        rain_duration = 5

        self.plotter.open_gif("rain_with_puddles_and_streams.gif")

        spheres_data = [
            {
                "position": [random.uniform(-25, 25), random.uniform(-25, 25), random.uniform(5, 15)],
                "speed": random.uniform(1.5, 2.0),
                "in_stream": False,
                "stream_position": None
            }
            for _ in range(num_drops)
        ]

        puddle_depth = unconfined_layer_depth + 0.5
        puddles = {}

        num_steps = 100
        for step in range(num_steps):
            self.plotter.clear()

            for layer in layers:
                plane = pv.Plane(center=(0, 0, layer["height"]), direction=(0, 0, 1), i_size=60, j_size=60)
                self.plotter.add_mesh(plane, color=layer["color"], opacity=layer["opacity"])

            for sphere_data in spheres_data:
                x, y, z = sphere_data["position"]
                z -= sphere_data["speed"]

                if z <= puddle_depth and not sphere_data["in_stream"]:
                    sphere_data["in_stream"] = True
                    puddle_key = (round(x), round(y))
                    if puddle_key in puddles:
                        puddles[puddle_key]["size"] += 0.05
                    else:
                        puddles[puddle_key] = {"size": 0.1, "depth": puddle_depth}

                if sphere_data["in_stream"]:
                    if sphere_data["stream_position"] is None:
                        sphere_data["stream_position"] = puddle_depth

                    if sphere_data["stream_position"] <= confined_layer_depth:
                        sphere_data["in_stream"] = False
                        sphere_data["stream_position"] = None
                        continue

                    zigzag_start = (x, y, sphere_data["stream_position"])
                    x_values, y_values, z_values = self.create_short_zigzag(zigzag_start, (0, 0, -1))

                    for i in range(len(x_values) - 1):
                        line_segment = pv.Line(pointa=(x_values[i], y_values[i], z_values[i]),
                                               pointb=(x_values[i + 1], y_values[i + 1], z_values[i + 1]))
                        self.plotter.add_mesh(line_segment, color="lightblue", line_width=2)

                    sphere_data["stream_position"] -= 0.3

                if not sphere_data["in_stream"]:
                    sphere = pv.Sphere(radius=drop_radius, center=(x, y, z))
                    self.plotter.add_mesh(sphere, color='blue', opacity=0.6)

            for puddle_pos, puddle_data in puddles.items():
                puddle_plane = pv.Circle(radius=puddle_data["size"], center=(puddle_pos[0], puddle_pos[1], puddle_data["depth"]))
                self.plotter.add_mesh(puddle_plane, color="lightblue", opacity=0.6)

            self.plotter.write_frame()

        self.plotter.close()

import pyvista as pv
import numpy as np
import random

class RainAnimation:
    def __init__(self):
        self.plotter = pv.Plotter()
        self.plotter.open_gif("rain_with_puddles_and_streams.gif")
        
        # Define layers with colors and positions to simulate soil depth
        self.layers = [
            {'center': (0, 0, -5), 'color': 'blue', 'opacity': 0.4},  # First layer with puddles
            {'center': (0, 0, -10), 'color': 'green', 'opacity': 0.3},
            {'center': (0, 0, -15), 'color': 'brown', 'opacity': 0.2},
            {'center': (0, 0, -20), 'color': 'gray', 'opacity': 0.1}  # Fourth layer, where streams disappear
        ]
        self.num_drops = 50  # Number of raindrops in animation
        self.steps = 100     # Steps for animation duration
        self.puddles = {}    # Dictionary to store puddle positions and sizes

    def setup_scene(self):
        """Sets up the soil layers and puddle plane."""
        for layer in self.layers:
            plane = pv.Plane(center=layer['center'], direction=(0, 0, 1), i_size=20, j_size=20)
            self.plotter.add_mesh(plane, color=layer['color'], opacity=layer['opacity'])
        
        # Plane for puddles
        self.puddle_layer = pv.Plane(center=(0, 0, -5), direction=(0, 0, 1), i_size=20, j_size=20)
        self.plotter.add_mesh(self.puddle_layer, color='lightblue', opacity=0.6)

    def create_zigzag_stream(self, start, length=1.0, amplitude=0.2):
        """Creates a zigzag stream for water flow."""
        x_values = np.linspace(start[0], start[0], 10)
        y_values = np.linspace(start[1], start[1], 10)
        z_values = np.linspace(start[2], start[2] - length, 10)

        for i in range(1, len(z_values) - 1):
            x_values[i] += np.random.uniform(-amplitude, amplitude)
            y_values[i] += np.random.uniform(-amplitude, amplitude)

        return x_values, y_values, z_values

    def animate_rain(self):
        """Simulates raindrops creating puddles and streams in the soil layers."""
        # Initial positions of raindrops
        drops = [{'position': [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(5, 15)], 
                  'is_stream': False} for _ in range(self.num_drops)]

        for step in range(self.steps):
            self.plotter.clear()  # Clear plot for each animation frame

            # Redraw soil layers and puddle plane
            self.setup_scene()

            for drop in drops:
                x, y, z = drop['position']
                z -= 0.2  # Drop falls each step

                # If drop reaches the puddle layer, create or expand a puddle
                if z <= -5 and not drop['is_stream']:
                    drop['is_stream'] = True
                    puddle_key = (round(x), round(y))
                    
                    # Create or increase the size of the puddle at this location
                    if puddle_key in self.puddles:
                        self.puddles[puddle_key] += 0.1  # Increase puddle size
                    else:
                        self.puddles[puddle_key] = 0.3   # Initial size of the new puddle
                    continue

                # If drop is in stream mode, create a zigzag stream downwards
                if drop['is_stream']:
                    x_values, y_values, z_values = self.create_zigzag_stream((x, y, z), length=5)

                    # Draw each segment of the stream
                    for i in range(len(z_values) - 1):
                        line_segment = pv.Line(pointa=(x_values[i], y_values[i], z_values[i]),
                                               pointb=(x_values[i + 1], y_values[i + 1], z_values[i + 1]))
                        self.plotter.add_mesh(line_segment, color='lightblue', line_width=3)

                    # Stop stream if it reaches the last layer
                    if z <= -20:
                        drop['is_stream'] = False

                # If drop is still falling, show it as a small sphere
                if not drop['is_stream']:
                    sphere = pv.Sphere(radius=0.1, center=(x, y, z))
                    self.plotter.add_mesh(sphere, color='lightblue')

                # Update drop position
                drop['position'] = [x, y, z]

            # Draw all puddles using pv.Disc
            for (px, py), size in self.puddles.items():
                puddle = pv.Disc(center=(px, py, -5), inner=0, outer=size, normal=(0, 0, 1))
                self.plotter.add_mesh(puddle, color="lightblue", opacity=0.6)

            # Write frame for GIF
            self.plotter.write_frame()

    def close_animation(self):
        """Finalizes and closes the animation file."""
        self.plotter.close()

# Run the animation
animation = RainAnimation()
animation.setup_scene()
animation.animate_rain()
animation.close_animation()

print("GIF saved as 'rain_with_puddles_and_streams.gif'")
