import pandas as pd
from tkinter import filedialog

class DataPreprocessing:
    def __init__(self):
        self.data_descriptors = {
            "precipitation": None,
            "soil": None,
            "well": None,
            "infiltration": None
        }

    def load_data(self, data_type):
        file_path = filedialog.askopenfilename()
        if not file_path:
            print(f"No file selected for {data_type}.")
            return

        try:
            if data_type == "well":
                data = pd.read_csv(file_path)
            else:
                data = pd.read_excel(file_path, engine='openpyxl')
            self.data_descriptors[data_type] = data
        except Exception as e:
            raise ValueError(f"Failed to load {data_type} data: {e}")

    def get_unique_values(self, data_type, column_name):
        data = self.data_descriptors.get(data_type)
        if data is not None and column_name in data.columns:
            return data[column_name].unique().tolist()
        else:
            return []

    def get_filtered_data(self, timestamp=None, region=None, timeseries=None, month=None):
        filtered_data = {}

        if timestamp:
            well_data = self.data_descriptors["well"]
            filtered_data["well"] = well_data[well_data["Timestamp"] == int(timestamp)] if well_data is not None else None

        if region:
            precipitation_data = self.data_descriptors["precipitation"]
            if precipitation_data is not None:
                filtered_precipitation = precipitation_data[precipitation_data["Region"] == region]
                if month and month in filtered_precipitation.columns:
                    filtered_data["precipitation"] = filtered_precipitation[["Region", month]]
                else:
                    filtered_data["precipitation"] = filtered_precipitation
            else:
                filtered_data["precipitation"] = None

        if timeseries:
            infiltration_data = self.data_descriptors["infiltration"]
            filtered_data["infiltration"] = infiltration_data[infiltration_data["Timeseries"] == int(timeseries)] if infiltration_data is not None else None

        filtered_data["soil"] = self.data_descriptors["soil"]
        
        return filtered_data