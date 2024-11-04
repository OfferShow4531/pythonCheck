import pyvista as pv
import numpy as np
import random
from modelling import Prototype

class Plot:
    def __init__(self):
        self.plotter = pv.Plotter()
        self.layers = [
            {'name': 'Organic', 'height': 2, 'color': 'saddlebrown', 'opacity': 1.0, 'permeability': 0.1},
            {'name': 'Surface', 'height': 3, 'color': 'forestgreen', 'opacity': 0.6, 'permeability': 0.5},
            {'name': 'Subsoil', 'height': 4, 'color': 'sandybrown', 'opacity': 0.7, 'permeability': 0.3},
            {'name': 'Unconfined Aquifer', 'height': 5, 'color': 'skyblue', 'opacity': 0.4, 'permeability': 0.8},
            {'name': 'Confined Layer', 'height': 4, 'color': 'gray', 'opacity': 0.6, 'permeability': 0.2},
            {'name': 'Bedrock', 'height': 6, 'color': 'black', 'opacity': 1.0, 'permeability': 0.0}
        ]
        self.num_drops = 10
        self.steps = 120
        self.water_level = -15  # Начальный уровень воды в Confined Layer
        self.prototype = Prototype(self.plotter, self.layers, self.water_level)

    def make_3d_graph(self, x_coordinate, y_coordinate, z_coordinates, n_wells):
        """Создание 3D модели с использованием прототипа"""
        self.soil_meshes = self.prototype.draw_static_soil_layers()

        # Создание скважин
        offsets = np.linspace(-25, 25, n_wells)
        colors = ['blue', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'pink', 'brown', 'gray']
        for i in range(n_wells):
            well_position = (x_coordinate + offsets[i], y_coordinate)
            self.prototype.create_well(well_position[0], well_position[1], -15, colors[i % len(colors)])

        # Добавление растений
        self.plants = self.prototype.add_plants()

        # Инициализация капель дождя
        initial_positions = [[random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(5, 15)] for _ in range(self.num_drops)]
        self.drops, self.drop_actors = self.prototype.animate_rain(self.num_drops, initial_positions)

        # Запуск анимации
        self.plotter.open_gif("rain_and_pumping_animation.gif")
        self.animate_rain_and_pumping()
        self.plotter.close()

    def animate_rain_and_pumping(self):
        """Запуск анимации дождя, луж, инфильтрации и роста растений"""
        for step in range(self.steps):
            self.prototype.update_drops(self.drops, self.drop_actors)
            self.prototype.update_puddles()
            self.prototype.update_infiltration()
            self.prototype.update_plant_growth(self.plants)
            self.plotter.write_frame()

    def update_drops(self):
        """Обновление положения капель дождя"""
        for i, drop in enumerate(self.drops):
            x, y, z = drop['position']
            if z <= -2.5:  # Лужи на уровне Organic
                puddle_key = (round(x), round(y))
                self.puddles[puddle_key] = self.puddles.get(puddle_key, 0.3) + 0.1  # Увеличение лужи
                drop['position'] = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(5, 15)]  # Обновление позиции капли наверху
            else:
                z -= 0.2  # Падение капли вниз
                drop['position'] = [x, y, z]
                self.drop_actors[i].SetPosition(x, y, z)