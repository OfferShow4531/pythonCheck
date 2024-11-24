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
                print(f" - No infiltration data found for Timeseries = {timeseries}. Defaulting infiltration_rate to 0.")
                self.infiltration_rate = 0
            else:
                self.infiltration_rate = float(infiltration_row["Infiltration Rate"].values[0])
                print(f" - Infiltration Rate: {self.infiltration_rate}")

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
            self.add_wells(timeseries=timeseries)

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

        print("Drawing soil layers with realistic surface...")
        extended_bounds = (-100, 100, -100, 100)

        for _, row in self.soil_data.iterrows():
            depth_low = row['Soil Index Lower']
            depth_high = row['Soil Index Higher']
            color = colors.get(row['Soil Name'], "gray")
            
            if row['Soil Name'] == "Surface":
                # Создаём сетку для поверхности
                x = np.linspace(extended_bounds[0], extended_bounds[1], 50)
                y = np.linspace(extended_bounds[2], extended_bounds[3], 50)
                x, y = np.meshgrid(x, y)

                # Генерируем высоты с использованием шума Перлина (поэлементно)
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

                # Создаём поверхность
                surface = pv.StructuredGrid(x, y, z)
                self.plotter.add_mesh(surface, color=color, opacity=0.5)

                # Устанавливаем верхнюю границу поверхности
                self.surface_layer_top = depth_high

            else:
                # Обычные слои как раньше
                cube = pv.Box(bounds=(*extended_bounds, depth_low, depth_high))
                opacity = 0.3 if row['Soil Name'] != 'Bedrock' else 1.0
                self.plotter.add_mesh(cube, color=color, opacity=opacity)

        # Устанавливаем глобальные границы
        self.global_bounds = (*extended_bounds, self.soil_data['Soil Index Lower'].min(), self.soil_data['Soil Index Higher'].max())
        print(f"Global bounds set to: {self.global_bounds}")


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

        # Check if rain is present
        if timeseries > 300:
            print(" - Rain stops after timeseries 300.")
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
            else:
                print(" - No rain drops generated due to low intensity.")
        except Exception as e:
            print(f"Error adding precipitation effects: {e}")


    def add_infiltration_lines(self, timeseries, infiltration_rate, sandy_loam_depth):
        """Adding animated infiltration lines with flow toward sandy pits."""
        print("\nAdding infiltration lines with flow effect...")
        try:
            if self.global_bounds is None:
                print("Error: Global bounds are not set. Cannot add infiltration lines.")
                return

            num_lines = max(5, int((5000 - infiltration_rate) / 100))
            print(f" - Number of infiltration lines: {num_lines}")

            for _ in range(num_lines):
                x_start = np.random.uniform(-100, 100)
                y_start = np.random.uniform(-100, 100)
                start_depth = self.surface_layer_top

                # Target sandy pit
                x_target = np.random.choice(np.linspace(-50, 50, 10))
                y_target = 0
                z_target = sandy_loam_depth

                # Adjust flow speed based on timeseries
                flow_factor = max(0.2, min((420 - timeseries) / 240, 1))  # Decreases until timeseries = 420
                for i in range(int(10 * flow_factor)):
                    x_values = np.linspace(x_start, x_target, i + 2)
                    y_values = np.linspace(y_start, y_target, i + 2)
                    z_values = np.linspace(start_depth, z_target, i + 2)

                    points = np.column_stack((x_values, y_values, z_values))
                    self.plotter.add_points(points, color='blue', point_size=5, render_points_as_spheres=True)

        except Exception as e:
            print(f"Error adding infiltration lines: {e}")

    
    def _add_final_infiltration(self, sandy_loam_depth):
        """Simulate the final infiltration effect at the sandy pit."""
        for i in range(200):
            x_point = np.random.uniform(-50, 50)
            y_point = np.random.uniform(-10, 10)
            z_point = sandy_loam_depth - np.random.uniform(0, 2)

            self.plotter.add_points([[x_point, y_point, z_point]], color='skyblue', point_size=5, render_points_as_spheres=True)


    def add_puddles(self, infiltration_rate):
        """Adding puddles over expanded area based on rainfall and infiltration rate."""
        print("\nAdding puddles...")

        # Проверяем, что уровень поверхности установлен
        if self.surface_layer_top is None:
            print("Error: Surface layer top is not set. Cannot add puddles.")
            return

        try:
            puddle_factor = 1 - min(infiltration_rate / 5000, 1)  # Меньше луж при высоком уровне инфильтрации
            num_puddles = max(1, int(30 * puddle_factor))  # Минимум 1 лужа

            for _ in range(num_puddles):
                x = np.random.uniform(-100, 100)  # Случайная позиция по X
                y = np.random.uniform(-100, 100)  # Случайная позиция по Y
                radius = np.random.uniform(1, 5)  # Размер лужи

                # Создаём лужу как диск
                puddle = pv.Disc(
                    center=(x, y, self.surface_layer_top - 0.1),  # Чуть ниже уровня поверхности
                    inner=0,  # Внутренний радиус
                    outer=radius,  # Внешний радиус
                    normal=(0, 0, 1)  # Плоскость диска перпендикулярна Z
                )
                self.plotter.add_mesh(puddle, color='cyan', opacity=0.5)

            print(f" - Added {num_puddles} puddles.")
        except Exception as e:
            print(f"Error adding puddles: {e}")

    def add_wells(self, timeseries):
        """Add wells with associated pits and dynamic water levels."""
        print("\nAdding wells with pits and dynamic water levels...")
        surface_level = self.soil_data.loc[self.soil_data['Soil Name'] == 'Surface', 'Soil Index Higher'].values[0]
        sandy_loam_depth = self.soil_data.loc[self.soil_data['Soil Name'] == 'Sandy Loam', 'Soil Index Lower'].values[0]
        groundwater_depth = self.soil_data.loc[self.soil_data['Soil Name'] == 'Groundwater', 'Soil Index Lower'].values[0]

        n_wells = len(self.well_data.columns)
        x_positions = np.linspace(-50, 50, n_wells + 1)

        for x_position in x_positions:
            # Add well structure
            well_cylinder = pv.Cylinder(
                center=(x_position, 0, (surface_level + groundwater_depth) / 2),
                direction=(0, 0, -1),
                height=abs(surface_level - groundwater_depth),
                radius=1.5
            )
            self.plotter.add_mesh(well_cylinder, color='gray', opacity=0.9)

            # Add water level
            water_height = groundwater_depth + (self.infiltration_rate / 5000 * (surface_level - groundwater_depth))
            water_cylinder = pv.Cylinder(
                center=(x_position, 0, (groundwater_depth + water_height) / 2),
                direction=(0, 0, -1),
                height=abs(groundwater_depth - water_height),
                radius=1.4
            )
            self.plotter.add_mesh(water_cylinder, color='blue', opacity=0.5)

            # Add pump or fountain based on timeseries
            if timeseries >= 480:
                self._add_pump(x_position, 0, groundwater_depth)
            if timeseries == 540:
                self.add_fountain(x_position, 0, surface_level)

        # Add pits
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
        print("\nAdding water vortex effect...")
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
        print("\nAdding pump system at timeseries = 480...")
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
        print("\nAdding water fountain at timeseries = 540...")
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
                
