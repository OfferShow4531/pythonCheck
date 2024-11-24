import pyvista as pv
import numpy as np
import pandas as pd
import random
import noise

class Plot3D:
    def __init__(self, soil_data, precipitation_data, infiltration_data, well_data):
        self.plotter = pv.Plotter()
        self.soil_data = soil_data
        self.precipitation_data = precipitation_data
        self.infiltration_data = infiltration_data
        self.well_data = well_data
        self.infiltration_rate = 0
        self.precipitation_value = 0
        # Initialize default global bounds and surface layer top
        self.global_bounds = None
        self.surface_layer_bottom = self.soil_data.loc[self.soil_data['Soil Name'] == 'Surface', 'Soil Index Lower'].min()

        print("Initialization complete:")
        print(f" - Soil data:\n{self.soil_data}")
        print(f" - Precipitation data:\n{self.precipitation_data}")
        print(f" - Infiltration data:\n{self.infiltration_data}")
        print(f" - Well data:\n{self.well_data}")

    def make_3d_model(self, region, month, timeseries):
        """Create the full 3D model."""
        try:
            print("\nCreating 3D model...\n")
            timeseries = int(timeseries)
            print(f" - Selected Timeseries: {timeseries}")

            # Filter infiltration data based on Timeseries
            infiltration_row = self.infiltration_data[self.infiltration_data["Timeseries"] == timeseries]
            if infiltration_row.empty:
                print(f"[DEBUG] Infiltration data not found for Timeseries = {timeseries}. Setting infiltration_rate = 0.")
                self.infiltration_rate = 0
            else:
                self.infiltration_rate = float(infiltration_row["Infiltration Rate"].values[0])
                print(f"[DEBUG] Infiltration data found: {infiltration_row}")
                print(f"[DEBUG] Calculated Infiltration Rate: {self.infiltration_rate}")

            # Filter precipitation data based on region
            precipitation_row = self.precipitation_data.loc[self.precipitation_data["Region"] == region]
            if not precipitation_row.empty and month in precipitation_row.columns:
                self.precipitation_value = float(precipitation_row[month].values[0])
                print(f" - Precipitation value for {region} in {month}: {self.precipitation_value}")
            else:
                self.precipitation_value = 0.0
                print(f" - No precipitation data found for region '{region}' and month '{month}'.")

            # Retrieve depths for sandy loam and medium loam layers
            sandy_loam_depth = self.soil_data.loc[self.soil_data['Soil Name'] == 'Sandy Loam', 'Soil Index Lower'].values[0]

            # Create soil layers, plants, and other elements of the model
            self.draw_soil_layers()
            self.add_plants(timeseries=timeseries)
            self.add_precipitation_effects(
                month=month,
                region=region,
                timeseries=timeseries,
                precipitation_value=self.precipitation_value,
                infiltration_rate=self.infiltration_rate
            )
            self.add_infiltration_lines(timeseries=timeseries, infiltration_rate=self.infiltration_rate, sandy_loam_depth=sandy_loam_depth)
            self.add_puddles(infiltration_rate=self.infiltration_rate)
            self.add_legend(self.plotter, elements=["Surface Layer", "Plants", "Puddles", "Wells", "Pump"])
            self.add_wells()

            self.plotter.show()
        except Exception as e:
            print(f"Error creating 3D model: {e}")


    def draw_soil_layers(self):
        """Draw soil layers with realistic surface heights."""
        colors = {
            "Surface": "green", "Sandy": "yellow", "Sandy Loam": "gold",
            "Light Loam": "orange", "Medium Loam": "#ff4500", "Heavy Loam": "brown",
            "Clay": "#8b4513", "Groundwater": "blue", "Mineral": "gray", "Bedrock": "black"
        }

        print("[DEBUG] Starting to draw soil layers...")
        extended_bounds = (-100, 100, -100, 100)

        for _, row in self.soil_data.iterrows():
            depth_low = row['Soil Index Lower']
            depth_high = row['Soil Index Higher']
            color = colors.get(row['Soil Name'], "gray")

            print(f"[DEBUG] Processing soil layer: {row['Soil Name']} with depth range ({depth_low}, {depth_high})")

            if row['Soil Name'] == "Surface":
                # Генерируем поверхность с шумом Перлина
                x = np.linspace(extended_bounds[0], extended_bounds[1], 50)
                y = np.linspace(extended_bounds[2], extended_bounds[3], 50)
                x, y = np.meshgrid(x, y)

                z = np.zeros_like(x)
                for i in range(x.shape[0]):
                    for j in range(x.shape[1]):
                        z[i, j] = depth_high + noise.pnoise2(
                            x[i, j] / 50.0,
                            y[i, j] / 50.0,
                            octaves=3,
                            persistence=0.5,
                            lacunarity=2.0
                        ) * 5
                        if i == 0 and j == 0:  # Печатаем примерное значение для первого узла
                            print(f"[DEBUG] Noise value at (0, 0): {z[i, j]}")

                surface = pv.StructuredGrid(x, y, z)
                self.plotter.add_mesh(surface, color=color, opacity=0.5)

                self.surface_layer_top = depth_high
                print(f"[DEBUG] Set surface_layer_top to {self.surface_layer_top}")
            else:
                # Добавляем куб для других слоёв
                cube = pv.Box(bounds=(*extended_bounds, depth_low, depth_high))
                opacity = 0.3 if row['Soil Name'] != 'Bedrock' else 1.0
                self.plotter.add_mesh(cube, color=color, opacity=opacity)

        # Устанавливаем глобальные границы
        self.global_bounds = (*extended_bounds, self.soil_data['Soil Index Lower'].min(), self.soil_data['Soil Index Higher'].max())
        print(f"[DEBUG] Global bounds set to: {self.global_bounds}")


    def add_plants(self, timeseries):
        """Add plants with dynamic growth."""
        print("\nAdding plants with growth...")

        if pd.isna(self.surface_layer_bottom):
            print("Error: Surface layer bottom is not set or cannot be determined. Cannot add plants.")
            return

        num_plants = 150
        growth_factor = 1 + (timeseries / 60)  # Plants grow as timeseries increases

        for i in range(num_plants):
            x = np.random.uniform(-100, 100)  # Random X position
            y = np.random.uniform(-100, 100)  # Random Y position
            height = 1.0 * growth_factor  # Plant height scales with growth factor

            # Устанавливаем уровень Z для растений на 10 выше уровня минимального Soil Index Lower
            z_position = self.surface_layer_bottom - 3 + height / 2

            plant = pv.Cylinder(
                center=(x, y, z_position),  # Устанавливаем правильную координату Z
                radius=0.1,
                height=height,
                direction=(0, 0, 1)
            )
            self.plotter.add_mesh(plant, color='darkgreen', opacity=0.9)


    def add_precipitation_effects(self, month, region, timeseries, precipitation_value, infiltration_rate):
        """Adding dynamic precipitation effects based on rainfall and infiltration rate."""
        print("\nAdding precipitation effects...")

        if timeseries > 300:
            print(" - Rain stops after timeseries 300.")
            self.rain_points = np.empty((0, 3))  # Очистить данные дождя
            return

        try:
            rain_intensity = max(0, 1 - (timeseries / 300))  # Rain decreases with time
            num_drops = int(precipitation_value * 10 * rain_intensity)

            if num_drops > 0:
                x_positions = np.random.uniform(-100, 100, num_drops)
                y_positions = np.random.uniform(-100, 100, num_drops)
                z_positions = np.full(num_drops, self.surface_layer_top - 10)

                rain_points = np.column_stack((x_positions, y_positions, z_positions))
                self.plotter.add_points(rain_points, color='blue', point_size=5, render_points_as_spheres=True)

                # Сохраняем точки дождя для мониторинга
                self.rain_points = rain_points
            else:
                print(" - No rain drops generated due to low intensity.")
                self.rain_points = np.empty((0, 3))  # Очистить данные дождя
        except Exception as e:
            print(f"Error adding precipitation effects: {e}")


    def add_infiltration_lines(self, timeseries, infiltration_rate, sandy_loam_depth):
        """Adding animated infiltration lines with flow toward sandy pits."""
        print("\nAdding infiltration lines with flow effect...")
        try:
            if self.global_bounds is None:
                print("Error: Global bounds are not set. Cannot add infiltration lines.")
                self.infiltration_lines = []  # Очистить линии инфильтрации
                return

            num_lines = max(5, int((5000 - infiltration_rate) / 100))
            print(f" - Number of infiltration lines: {num_lines}")

            infiltration_points = []

            for _ in range(num_lines):
                x_start = np.random.uniform(-100, 100)
                y_start = np.random.uniform(-100, 100)
                z_start = self.surface_layer_top

                x_target = np.random.uniform(-50, 50)
                y_target = np.random.uniform(-50, 50)
                z_target = sandy_loam_depth

                x_values = np.linspace(x_start, x_target, 10)
                y_values = np.linspace(y_start, y_target, 10)
                z_values = np.linspace(z_start, z_target, 10)

                points = np.column_stack((x_values, y_values, z_values))
                infiltration_points.extend(points)

                self.plotter.add_points(points, color='blue', point_size=5, render_points_as_spheres=True)

            # Сохраняем данные инфильтрации
            self.infiltration_lines = infiltration_points
        except Exception as e:
            print(f"Error adding infiltration lines: {e}")


    def add_puddles(self, infiltration_rate):
        """Adding puddles over expanded area based on rainfall and infiltration rate."""
        print("\nAdding puddles...")

        if self.surface_layer_top is None:
            print("Error: Surface layer top is not set. Cannot add puddles.")
            return

        try:
            puddle_factor = 1 - min(infiltration_rate / 5000, 1)  # Меньше луж при высоком уровне инфильтрации
            num_puddles = max(1, int(30 * puddle_factor))  # Минимум 1 лужа
            puddle_radii = []

            for _ in range(num_puddles):
                x = np.random.uniform(-100, 100)
                y = np.random.uniform(-100, 100)
                radius = np.random.uniform(1, 5)  # Размер лужи
                puddle_radii.append(radius)

                puddle = pv.Disc(
                    center=(x, y, self.surface_layer_top - 0.1),
                    inner=0,
                    outer=radius,
                    normal=(0, 0, 1)
                )
                self.plotter.add_mesh(puddle, color='cyan', opacity=0.5)

            # Сохраняем данные о лужах
            self.puddles_data = puddle_radii
            print(f" - Added {num_puddles} puddles.")
        except Exception as e:
            print(f"Error adding puddles: {e}")
    
    def monitor_simulation(self):
        """Monitor the state of the simulation dynamically and calculate trends."""
        print("\n[MONITOR] Monitoring simulation state...")

        # Количество точек дождя (интенсивность дождя)
        rain_points = getattr(self, "rain_points", np.empty((0, 3)))
        rain_intensity_dynamic = len(rain_points) / 1000  # Нормализуем (например, 1000 точек = интенсивность 1)
        print(f" - Dynamic Rain Intensity: {rain_intensity_dynamic}")

        # Объем луж (площадь всех луж)
        puddles_data = getattr(self, "puddles_data", [])
        puddles_volume = sum(p**2 for p in puddles_data) * np.pi  # Пример: площадь луж
        print(f" - Dynamic Puddles Volume: {puddles_volume}")

        # Текущая инфильтрация
        infiltration_lines = getattr(self, "infiltration_lines", [])
        infiltration_dynamic = len(infiltration_lines) / 1000  # Нормализация
        print(f" - Dynamic Infiltration Rate: {infiltration_dynamic}")

        # Инициализация истории параметров
        if not hasattr(self, "history"):
            self.history = {"rain": [rain_intensity_dynamic], "puddles": [puddles_volume], "infiltration": [infiltration_dynamic]}
        else:
            # Добавляем текущие значения в историю
            self.history["rain"].append(rain_intensity_dynamic)
            self.history["puddles"].append(puddles_volume)
            self.history["infiltration"].append(infiltration_dynamic)

            # Ограничиваем историю до последних 10 шагов
            self.history["rain"] = self.history["rain"][-10:]
            self.history["puddles"] = self.history["puddles"][-10:]
            self.history["infiltration"] = self.history["infiltration"][-10:]

        return rain_intensity_dynamic, puddles_volume, infiltration_dynamic

    def add_wells(self):
        """Add wells with associated pits and dynamic water levels."""
        print("\nAdding wells with pits and dynamic water levels...")

        # Сбор текущих данных и трендов
        rain_intensity_dynamic, puddles_volume, infiltration_dynamic = self.monitor_simulation()

        # Расчет водного баланса
        water_balance = (rain_intensity_dynamic + puddles_volume / 1000) - infiltration_dynamic
        print(f" - Water Balance: {water_balance}")

        # Логика активации насоса
        activate_pump = False

        if water_balance > 0.5:
            print("[INFO] Activating artificial water extraction due to positive water balance.")
            activate_pump = True
        elif puddles_volume > 700 and infiltration_dynamic < 0.4:
            print("[INFO] Activating artificial water extraction due to increasing puddles and insufficient infiltration.")
            activate_pump = True
        elif puddles_volume > 800:
            print("[INFO] Activating artificial water extraction due to excessive puddles.")
            activate_pump = True
        else:
            print("[INFO] No need to activate pumping at this time.")
            
        # Уровни слоёв
        surface_level = self.soil_data.loc[self.soil_data['Soil Name'] == 'Surface', 'Soil Index Higher'].values[0]
        sandy_loam_depth = self.soil_data.loc[self.soil_data['Soil Name'] == 'Sandy Loam', 'Soil Index Lower'].values[0]
        groundwater_depth = self.soil_data.loc[self.soil_data['Soil Name'] == 'Groundwater', 'Soil Index Lower'].values[0]

        # Количество скважин
        n_wells = len(self.well_data.columns)
        x_positions = np.linspace(-50, 50, n_wells + 1)

        for x_position in x_positions:
            # Добавляем структуру скважины
            well_cylinder = pv.Cylinder(
                center=(x_position, 0, (surface_level + groundwater_depth) / 2),
                direction=(0, 0, -1),
                height=abs(surface_level - groundwater_depth),
                radius=1.5
            )
            self.plotter.add_mesh(well_cylinder, color='gray', opacity=0.9)

            # Уровень воды
            water_height = groundwater_depth + (self.infiltration_rate / 5000 * (surface_level - groundwater_depth))
            water_cylinder = pv.Cylinder(
                center=(x_position, 0, (groundwater_depth + water_height) / 2),
                direction=(0, 0, -1),
                height=abs(groundwater_depth - water_height),
                radius=1.4
            )
            self.plotter.add_mesh(water_cylinder, color='blue', opacity=0.5)

            # Активируем насосы, если нужно
            if activate_pump:
                self._add_pump(x_position, 0, groundwater_depth)

        # Добавляем песчаные карьеры
        self.add_pits(x_positions, sandy_loam_depth, groundwater_depth)


    def add_pits(self, well_x_positions, sandy_loam_depth, medium_loam_depth):
        """Add sand and gravel pits with tapering cylinders and vortex effect."""
        print("\nAdding sand and gravel pits with vortex effect...")
        for x in well_x_positions:
            # Sand Pit (Outer)
            sand_outer = pv.Cylinder(
                center=(x, 0, sandy_loam_depth - 2),
                direction=(0, 0, -1),
                height=8,
                radius=4.5,
                capping=True
            )
            self.plotter.add_mesh(sand_outer, color='gold', opacity=0.6)

            # Sand Pit (Inner)
            sand_inner = pv.Cylinder(
                center=(x, 0, sandy_loam_depth - 2),
                direction=(0, 0, -1),
                height=8,
                radius=2.5,
                capping=True
            )
            self.plotter.add_mesh(sand_inner, color='yellow', opacity=0.8)

            # Gravel Pit (Inner)
            gravel_inner = pv.Cylinder(
                center=(x, 0, medium_loam_depth - 2),
                direction=(0, 0, -1),
                height=8,
                radius=2.5,
                capping=True
            )
            self.plotter.add_mesh(gravel_inner, color='brown', opacity=0.8)

            # Water vortex effect
            self._add_water_vortex(x, sandy_loam_depth, medium_loam_depth)

    def _add_water_vortex(self, x, sandy_loam_depth, medium_loam_depth):
        """Add water vortex effect around the sand pit."""
        # print("\nAdding water vortex effect...")
        vortex_points = []

        for i in range(200):  # Генерация точек для воронки
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0.5, 3)
            height = np.random.uniform(sandy_loam_depth, medium_loam_depth)

            x_point = x + radius * np.cos(angle)
            y_point = radius * np.sin(angle)
            vortex_points.append([x_point, y_point, height])

        vortex_points = np.array(vortex_points)
        self.plotter.add_points(
            vortex_points, color='blue', point_size=5, render_points_as_spheres=True
        )

    def _add_pump(self, x, y, groundwater_depth):
        """Add a pump system for a well with dynamic extraction animation."""
        # print("\nAdding pump system at timeseries = 480...")
        for i in range(10):  # Simulate extraction with water level decrease
            pump = pv.Cylinder(
                center=(x, y, groundwater_depth + 2 + i),
                direction=(0, 0, -1),
                height=4,
                radius=0.5
            )
            self.plotter.add_mesh(pump, color='blue', opacity=1.0)

            vortex = pv.Cylinder(
                center=(x, y, groundwater_depth + i),
                direction=(0, 0, -1),
                height=3,
                radius=2
            )
            self.plotter.add_mesh(vortex, color='cyan', opacity=0.6)

    def add_fountain(self, x, y, surface_level):
        """Add a fountain for a well."""
        # print("\nAdding water fountain at timeseries = 540...")
        for i in range(10):  # Simulate water jet animation
            fountain = pv.Cone(
                center=(x, y, surface_level + (3 * i)),  # Increase height over time
                direction=(0, 0, 1),
                height=6,
                radius=1
            )
            self.plotter.add_mesh(fountain, color='skyblue', opacity=0.9)
        
    
    def add_legend(self, plotter, elements):
        """Add legend dynamically based on created elements."""
        legend_entries = {
            "Surface Layer": "green",
            "Sandy Layer": "yellow",
            "Sandy Loam": "gold",
            "Light Loam": "orange",
            "Medium Loam": "#ff4500",
            "Heavy Loam": "brown",
            "Clay Layer": "#8b4513",
            "Groundwater": "blue",
            "Plants": "darkgreen",
            "Puddles": "cyan",
            "Wells": "gray",
            "Pump": "purple",
        }

        try:
            filtered_entries = [(name, color) for name, color in legend_entries.items() if name in elements]
            plotter.add_legend(labels=filtered_entries, bcolor="white", loc="upper right")
        except Exception as e:
            print(f"Error adding legend: {e}")
                
