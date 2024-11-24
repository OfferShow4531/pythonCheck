import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Plot2D:
    def __init__(self, soil_data=None, precipitation_data=None, infiltration_data=None, well_data=None):
        self.soil_data = soil_data
        self.precipitation_data = precipitation_data
        self.infiltration_data = infiltration_data
        self.well_data = well_data

        # Create a figure and axis for plotting
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.added_labels = set()  # Для отслеживания уникальных меток в легенде
        print("Plot2D instance created.")

    def make_2d_projection(self, month, timeseries):
        """Creates the full 2D soil model."""
        print("Creating 2D Model...")
        self.draw_soil_layers()
        if self.precipitation_data is not None:
            precipitation_value = self.get_precipitation_value(month)
            self.add_precipitation(timeseries, precipitation_value)
        if self.infiltration_data is not None:
            self.add_infiltration(timeseries)
        if self.well_data is not None:
            self.add_wells(timeseries)
        self.add_puddles(timeseries)
        self.show()

    def draw_soil_layers(self):
        """Draws soil layers as horizontal bands."""
        print("Drawing soil layers...")
        colors = {
            "Surface": "green", "Sandy": "yellow", "Sandy Loam": "gold",
            "Light Loam": "orange", "Medium Loam": "#ff4500", "Heavy Loam": "brown",
            "Clay": "#8b4513", "Groundwater": "blue", "Mineral": "gray", "Bedrock": "black"
        }

        if self.soil_data is None or self.soil_data.empty:
            print("No soil data provided.")
            return

        for _, row in self.soil_data.iterrows():
            depth_low = row['Soil Index Lower']
            depth_high = row['Soil Index Higher']
            color = colors.get(row['Soil Name'], "gray")
            self.ax.fill_betweenx([depth_low, depth_high], -50, 50, color=color, alpha=0.5)

        self.ax.invert_yaxis()  # Depths go downward
        self.ax.set_title("2D Soil Model")
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Depth")

    def get_precipitation_value(self, month):
        """Fetches precipitation value for the month column."""
        print("Fetching precipitation value...")
        if not self.precipitation_data.empty:
            if month in self.precipitation_data.columns:
                return float(self.precipitation_data.iloc[0][month])
        print(f"No precipitation data available for {month}.")
        return 0

    def add_precipitation(self, timeseries, precipitation_value):
        """Adds raindrops based on precipitation data."""
        timeseries = int(timeseries)
        print("Adding precipitation...")
        if timeseries > 180:
            print("Rain animation stopped.")
            return

        num_drops = int(precipitation_value * 10)
        intensity_factor = max(0, 1 - max(0, timeseries - 60) / 120)

        num_drops = int(num_drops * intensity_factor)
        x_positions = np.random.uniform(-50, 50, num_drops)
        y_positions = np.random.uniform(-10, 0, num_drops)  # Above the surface
        self.ax.scatter(x_positions, y_positions, color='blue', s=5, label="Rain Drops")

    def add_infiltration(self, timeseries):
        """Добавляет извилистые и равномерно распределённые линии инфильтрации."""
        timeseries = int(timeseries)
        infiltration_row = self.infiltration_data[self.infiltration_data["Timeseries"] == timeseries]
        if not infiltration_row.empty:
            infiltration_rate = float(infiltration_row.iloc[0]["Infiltration Rate"])
            
            # Чем меньше `Infiltration Rate`, тем больше линий
            num_lines = max(5, int(5000 / infiltration_rate))  # Инвертируем пропорцию, минимум 5 линий
            
            for _ in range(num_lines):
                x_start = np.random.uniform(-50, 50)  # Случайная стартовая позиция по X
                y_positions = np.linspace(5, 35, 20)  # Равномерные точки по Y (глубина)
                
                # Случайные отклонения по X для создания извилистой линии
                x_positions = x_start + np.cumsum(np.random.uniform(-1, 1, size=len(y_positions)))

                if timeseries < 480:
                    # Рисуем извилистую линию
                    self.ax.plot(
                        x_positions,
                        y_positions,
                        color='cyan',
                        linewidth=1.2,
                        alpha=0.8,
                        label=self.add_to_legend("Infiltration")
                    )
        else:
            print(f"No infiltration data available for timeseries: {timeseries}")

    def add_wells(self, timeseries):
        """Добавляет скважины и визуализацию работы фонтана."""
        well_columns = [col for col in self.well_data.columns if col.startswith("Well")]
        n_wells = len(well_columns)
        well_spacing = 100 / (n_wells + 1)
        timeseries = int(timeseries)
        for i, col in enumerate(well_columns):
            x_position = -50 + (i + 1) * well_spacing
            # Рисуем основную скважину
            self.ax.plot([x_position, x_position], [3, 80], color='black', linewidth=2, label=self.add_to_legend("Well"))
            self.ax.plot([x_position - 2, x_position + 2], [10, 15], color='yellow', linewidth=4, label=self.add_to_legend("Sandy Funnel"))
            self.ax.plot([x_position - 3, x_position + 3], [20, 25], color='brown', linewidth=4, label=self.add_to_legend("Gravel Funnel"))

            # Добавляем анимацию выкачивания воды и фонтан при определённых значениях timeseries
            if timeseries >= 480:
                # Фонтан воды над скважиной
                fountain_height = np.linspace(0, 5, 10)
                fountain_spray_x = np.random.uniform(-2, 2, len(fountain_height)) + x_position
                self.ax.plot(fountain_spray_x, 80 + fountain_height, color='blue', alpha=0.8, label=self.add_to_legend("Fountain"))

                # Анимация выкачивания воды (распределение воды вокруг скважины)
                for _ in range(5):
                    scatter_x = x_position + np.random.uniform(-5, 5)
                    scatter_y = np.random.uniform(3, 10)
                    self.ax.scatter(scatter_x, scatter_y, color='cyan', s=30, alpha=0.6, label=self.add_to_legend("Pumped Water"))

        # Если timeseries == 540, добавляем дополнительные лужи
        if timeseries == 540:
            self.add_puddles(timeseries)

    def add_puddles(self, timeseries):
        """Добавляет лужи на уровне земли."""
        timeseries = int(timeseries)
        surface_level = 0  # Предположим, что уровень земли на отметке 0
        puddle_positions = np.random.uniform(-50, 50, 7)  # Увеличиваем количество луж
        if timeseries <= 420:
            for x in puddle_positions:
                self.ax.scatter(x, surface_level, color='blue', s=500, alpha=0.6, label=self.add_to_legend("Puddle"))

    def add_to_legend(self, label):
        """Добавляет элемент в легенду только один раз."""
        if label not in self.added_labels:
            self.added_labels.add(label)
            return label
        return '_nolegend_'

    def show(self):
        """Отображает график с легендой в правом верхнем углу."""
        self.ax.grid(True)
        self.ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.05))  # Легенда в правом верхнем углу за пределами графика
        plt.show()