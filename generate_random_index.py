import pandas as pd
import numpy as np

def generate_random_soil_data():
    """Generate random soil layer data."""
    soil_names = ["Surface", "Sandy", "Sandy Loam", "Light Loam", "Medium Loam", "Heavy Loam", "Clay", "Groundwater"]
    lower_bounds = np.arange(0, len(soil_names) * 10, 10)
    upper_bounds = lower_bounds + 10
    return pd.DataFrame({
        "Soil Name": soil_names,
        "Soil Index Lower": lower_bounds,
        "Soil Index Higher": upper_bounds
    })

def generate_random_precipitation_data():
    """Generate random precipitation data."""
    regions = ["RegionA", "RegionB", "RegionC"]
    months = ["January", "February", "March", "April"]
    data = {month: np.random.uniform(0, 100, len(regions)) for month in months}
    data["Region"] = regions
    return pd.DataFrame(data)

def generate_random_infiltration_data():
    """Generate random infiltration data."""
    timeseries = np.arange(0, 500, 60)
    infiltration_rates = np.random.uniform(0, 5000, len(timeseries))
    infiltration_speeds = np.random.uniform(0.1, 1.0, len(timeseries))
    water_consumption = np.random.uniform(100, 500, len(timeseries))
    return pd.DataFrame({
        "Timeseries": timeseries,
        "Infiltration Rate": infiltration_rates,
        "Infiltration Speed": infiltration_speeds,
        "Water consumption": water_consumption
    })

def generate_random_well_data():
    """Generate random well data."""
    timestamps = np.arange(1609459200, 1609459200 + 10 * 3600, 3600)  # 10 hours of data
    wells = {f"Well{i}": np.random.uniform(-10, 0, len(timestamps)) for i in range(1, 11)}
    wells["Timestamp"] = timestamps
    return pd.DataFrame(wells)


def generate_and_log(self, data_type, generator_function):
    """Генерирует случайные данные и логирует их создание."""
    print(f"{data_type} data missing. Generating random {data_type.lower()} data.")
    return generator_function()