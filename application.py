
import pandas as pd
import tkinter as tk
from tkinter import filedialog, Label, Button, Text, Scrollbar, Frame, OptionMenu, StringVar, messagebox, HORIZONTAL, VERTICAL
from dataPreprocessing import DataPreprocessing
from pyVistaPlot import Plot3D
from pyVista2DPlot import Plot2D

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D Model Visualization")
        self.geometry("1200x800")
        self.configure(bg="gray")
        self.data_processor = DataPreprocessing()
        
        # Variables for selected filters
        self.selected_timestamp = StringVar(value="Select Timestamp")
        self.selected_region = StringVar(value="Select Region")
        self.selected_timeseries = StringVar(value="Select Timeseries")
        self.selected_month = StringVar(value="Select Month")
        
        self.option_menus = {}
        self.text_areas = {}
        self.create_widgets()

    def create_widgets(self):
        # Menu frame
        menu_frame = Frame(self, bg="#4f4f4f", padx=10, pady=10)
        menu_frame.pack(side="left", fill="y")

        Label(menu_frame, text="MENU", bg="#4f4f4f", fg="white", font=("Helvetica", 16, "bold"), pady=10).pack(pady=(0, 15), fill="x")

        Button(menu_frame, text="Load Precipitation Data", command=lambda: self.load_and_display_data("precipitation"),
               bg="#5a5a5a", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=5, padx=5, fill="x")
        Button(menu_frame, text="Load Soil Data", command=lambda: self.load_and_display_data("soil"),
               bg="#5a5a5a", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=5, padx=5, fill="x")
        Button(menu_frame, text="Load Well Data", command=lambda: self.load_and_display_data("well"),
               bg="#5a5a5a", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=5, padx=5, fill="x")
        Button(menu_frame, text="Load Infiltration Data", command=lambda: self.load_and_display_data("infiltration"),
               bg="#5a5a5a", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=5, padx=5, fill="x")

        Button(menu_frame, text="Make 2D Model", command=self.make_2d_model,
               bg="#5a5a5a", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=5, padx=5, fill="x")
        Button(menu_frame, text="Make 3D Model", command=self.make_3d_model,
               bg="#5a5a5a", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=5, padx=5, fill="x")

        # Create option menus for filters
        self.option_menus["timestamp"] = OptionMenu(menu_frame, self.selected_timestamp, "Select Timestamp")
        self.option_menus["timestamp"].pack(pady=5, padx=5, fill="x")   
             
        self.option_menus["region"] = OptionMenu(menu_frame, self.selected_region, "Select Region")
        self.option_menus["region"].pack(pady=5, padx=5, fill="x")
        
        self.option_menus["timeseries"] = OptionMenu(menu_frame, self.selected_timeseries, "Select Timeseries")
        self.option_menus["timeseries"].pack(pady=5, padx=5, fill="x")     

        # New option menu for selecting month
        self.option_menus["month"] = OptionMenu(menu_frame, self.selected_month, "Select Month")
        self.option_menus["month"].pack(pady=5, padx=5, fill="x")
        
        Button(menu_frame, text="CLOSE", command=self.quit, bg="#d9534f", fg="white", font=("Helvetica", 12, "bold"), relief="flat").pack(pady=20, padx=5, fill="x")

        # Data display frame
        data_frame = Frame(self, bg="#d3d3d3")
        data_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Configure grid layout for the data frame
        data_frame.grid_rowconfigure(0, weight=1)
        data_frame.grid_rowconfigure(1, weight=1)
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_columnconfigure(1, weight=1)

        for data_type in ["well", "soil", "precipitation", "infiltration"]:
            self.text_areas[data_type] = self.create_text_area(data_frame, data_type.capitalize(), len(self.text_areas) // 2, len(self.text_areas) % 2)

    def create_text_area(self, parent, label_text, row, column):
        frame = Frame(parent, bg="#e6e6e6", padx=5, pady=5)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        # Конфигурация сетки для фрейма
        frame.grid_rowconfigure(0, weight=1)  # Текстовое поле
        frame.grid_columnconfigure(0, weight=1)  # Текстовое поле

        # Заголовок
        Label(frame, text=f"Current Data: {label_text}", bg="#e6e6e6", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")

        # Основной текстовый виджет
        text_area = Text(frame, height=21, width=55, wrap="none")  # wrap="none" отключает автоперенос текста
        text_area.grid(row=1, column=0, sticky="nsew")

        # Вертикальный скроллбар
        y_scrollbar = Scrollbar(frame, orient=VERTICAL, command=text_area.yview)
        y_scrollbar.grid(row=1, column=1, sticky="ns")
        text_area.config(yscrollcommand=y_scrollbar.set)

        # Горизонтальный скроллбар
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL, command=text_area.xview)
        x_scrollbar.grid(row=2, column=0, sticky="ew")
        text_area.config(xscrollcommand=x_scrollbar.set)

        return text_area

    def load_and_display_data(self, data_type):
        try:
            self.data_processor.load_data(data_type)
            data = self.data_processor.data_descriptors[data_type]
            
            # Проверяем, что data не является None перед доступом к нему
            if data is not None:
                self.text_areas[data_type].delete("1.0", tk.END)
                self.text_areas[data_type].insert("1.0", data.to_string())
                
                if data_type == "well":
                    self.update_timestamp_options()
                elif data_type == "precipitation":
                    self.update_region_options()
                    self.update_month_options(data)  # Update months
                elif data_type == "infiltration":
                    self.update_timeseries_options()  # Update timeseries after loading infiltration data
            else:
                messagebox.showerror("Error", f"No data loaded for {data_type}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def update_month_options(self, data):
        """Extracts month columns from precipitation data and updates month selection menu."""
        # Get month columns (assuming they start from January onwards in the precipitation dataset)
        month_columns = data.columns[1:]  # Skip the 'Region' column
        # print("Available month columns:", month_columns)
        self.update_option_menu(self.selected_month, month_columns, "month")

    def update_timestamp_options(self):
        timestamps = self.data_processor.get_unique_values("well", "Timestamp")
        self.update_option_menu(self.selected_timestamp, timestamps, "timestamp")

    def update_region_options(self):
        regions = self.data_processor.get_unique_values("precipitation", "Region")
        self.update_option_menu(self.selected_region, regions, "region")

    def update_timeseries_options(self):
        # print("Called update_timeseries_options")
        # Проверим, что таблица загружена и доступен столбец "Timeseries"
        infiltration_data = self.data_processor.data_descriptors["infiltration"]
        infiltration_data.columns = infiltration_data.columns.str.strip()  # Удаление пробелов из имен столбцов
        # print("Infiltration data columns:", infiltration_data.columns)
        
        timeseries_values = self.data_processor.get_unique_values("infiltration", "Timeseries")
        # print("Available timeseries values:", timeseries_values)
        self.update_option_menu(self.selected_timeseries, timeseries_values, "timeseries")

    def update_option_menu(self, variable, options, menu_name):
        menu = self.option_menus[menu_name]["menu"]
        menu.delete(0, "end")
        for option in options:
            menu.add_command(label=option, command=lambda value=option: variable.set(value))

    def make_2d_model(self):
        self._create_model(Plot2D, "2D Model created")

    def make_3d_model(self):
        self._create_model(Plot3D, "3D Model created")

    def _create_model(self, plot_class, success_message):
        timestamp, region, timeseries, month = self.selected_timestamp.get(), self.selected_region.get(), self.selected_timeseries.get(), self.selected_month.get()
        
        if timestamp == "Select Timestamp" or region == "Select Region" or timeseries == "Select Timeseries" or month == "Select Month":
            messagebox.showwarning("Warning", "Please select valid timestamp, region, timeseries, and month.")
            return
        
        # xpos, ypos = self.get_coordinates_by_timestamp(int(timestamp))
        
        # Получение отфильтрованных данных
        filtered_data = self.data_processor.get_filtered_data(timestamp=timestamp, region=region, timeseries=timeseries, month=month)
        print(filtered_data)
        plot_instance = plot_class(
            soil_data=filtered_data["soil"],
            precipitation_data=filtered_data["precipitation"],
            infiltration_data=filtered_data["infiltration"],
            well_data=filtered_data["well"]
        )
        
        if plot_class == Plot2D:
            plot_instance.make_2d_projection(month, timeseries)
        else:
            plot_instance.make_3d_model(region, month, timeseries)
        print(success_message)
        
    def get_coordinates_by_timestamp(self, timestamp):
        well_data = self.data_processor.data_descriptors["well"]
        row = well_data[well_data['Timestamp'] == timestamp]
        if not row.empty:
            return row["Xpos"].values[0], row["Ypos"].values[0]
        else:
            raise ValueError(f"No data found for timestamp {timestamp}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
