import pyvista as pv
import numpy as np
import random

class Prototype:
    def __init__(self, plotter, layers, water_level):
        self.plotter = plotter
        self.puddles = {}  # Лужи на поверхности
        self.water_level = water_level  # Уровень воды в Confined Layer
        self.layers = layers  # Сохраняем слои почвы
        self.water_actor = None  # Инициализация water_actor

    def draw_static_soil_layers(self):
        """Создание и отображение статических слоев почвы"""
        current_depth = 0
        soil_meshes = []
        for layer in self.layers:
            bottom_z = current_depth - layer['height']
            cube = pv.Box(bounds=(-30, 30, -30, 30, bottom_z, current_depth))
            soil_mesh = self.plotter.add_mesh(cube, color=layer['color'], opacity=layer['opacity'], label=layer['name'])
            soil_meshes.append(soil_mesh)
            current_depth = bottom_z

        # Слой воды для Confined Layer
        water_mesh = pv.Box(bounds=(-30, 30, -30, 30, self.water_level, self.water_level + 1))
        self.water_actor = self.plotter.add_mesh(water_mesh, color="blue", opacity=0.3)  # Сохраняем water_actor
        return soil_meshes

    def create_well(self, x, y, confined_depth, color):
        """Создание и отображение скважины"""
        well_height = abs(confined_depth)
        well_cylinder = pv.Cylinder(center=(x, y, confined_depth / 2), radius=0.5, height=well_height, direction=(0, 0, -1))
        return self.plotter.add_mesh(well_cylinder, color=color, opacity=0.9)

    def add_plants(self, num_plants=5):
        """Создание растений и их корней на уровне Organic"""
        plants = []
        for _ in range(num_plants):
            x, y = random.uniform(-10, 10), random.uniform(-10, 10)
            plant = pv.Cone(center=(x, y, -2.5), direction=(0, 0, 1), height=1.5, radius=0.3)
            root = pv.Line(pointa=(x, y, -2.5), pointb=(x, y, -3))
            plant_actor = self.plotter.add_mesh(plant, color="darkgreen")
            root_actor = self.plotter.add_mesh(root, color="sienna")
            plants.append({'plant_actor': plant_actor, 'root_actor': root_actor, 'growth_stage': 1, 'x': x, 'y': y})
        return plants

    def animate_rain(self, num_drops, initial_positions):
        """Инициализация капель дождя"""
        drops = [{'position': pos, 'is_falling': True} for pos in initial_positions]
        drop_actors = [self.plotter.add_mesh(pv.Sphere(radius=0.1, center=drop['position']), color='lightblue') for drop in drops]
        return drops, drop_actors

    def update_drops(self, drops, drop_actors):
        """Обновление положения капель дождя и формирование луж"""
        for i, drop in enumerate(drops):
            x, y, z = drop['position']
            if z <= -2.5:  # Падение на уровень Organic
                drop['is_falling'] = False
                puddle_key = (round(x), round(y))
                self.puddles[puddle_key] = self.puddles.get(puddle_key, 0.3) + 0.1  # Увеличение лужи
                drop['position'] = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(5, 15)]  # Сброс капли
            else:
                z -= 0.2
                drop['position'] = [x, y, z]
                drop_actors[i].SetPosition(x, y, z)

    def update_puddles(self):
        """Обновление луж на поверхности"""
        for (px, py), size in self.puddles.items():
            puddle = pv.Disc(center=(px, py, -2.5), inner=0, outer=size, normal=(0, 0, 1))
            self.plotter.add_mesh(puddle, color="lightblue", opacity=0.6)

    def update_infiltration(self):
        """Анимация инфильтрации из луж вниз через слои"""
        for (px, py), size in self.puddles.items():
            infiltration_depth = -2.5  # Начало инфильтрации из луж
            for layer in self.layers:
                if layer['permeability'] > 0:
                    infiltration_depth -= layer['height'] * layer['permeability']
                    infiltration_disc = pv.Disc(center=(px, py, infiltration_depth), inner=0, outer=size, normal=(0, 0, 1))
                    self.plotter.add_mesh(infiltration_disc, color="skyblue", opacity=0.2)
                    
                    # Пополнение грунтовых вод в Confined Layer
                    if infiltration_depth <= self.water_level:
                        self.water_level += 0.01  # Пополнение уровня воды
                        self.plotter.remove_actor(self.water_actor)
                        water_mesh = pv.Box(bounds=(-30, 30, -30, 30, self.water_level, self.water_level + 1))
                        self.water_actor = self.plotter.add_mesh(water_mesh, color="blue", opacity=0.3)  # Обновление water_actor

    def update_plant_growth(self, plants):
        """Рост растений в зависимости от уровня воды"""
        for plant_info in plants:
            if plant_info['growth_stage'] < 5:
                plant_info['growth_stage'] += 0.1
                self.plotter.remove_actor(plant_info['plant_actor'])
                self.plotter.remove_actor(plant_info['root_actor'])
                plant_info['plant_actor'] = self.plotter.add_mesh(
                    pv.Cone(center=(plant_info['x'], plant_info['y'], -2.5 + plant_info['growth_stage'] / 2),
                            direction=(0, 0, 1), height=1.5 + plant_info['growth_stage'], radius=0.3),
                    color="darkgreen"
                )
                plant_info['root_actor'] = self.plotter.add_mesh(
                    pv.Line(pointa=(plant_info['x'], plant_info['y'], -2.5),
                            pointb=(plant_info['x'], plant_info['y'], -3 - plant_info['growth_stage'] / 2)),
                    color="sienna"
                )