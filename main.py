import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from descriptor import DataDescriptor
from pyVistaPlot import Plot


import tkinter as tk

data = DataDescriptor()
plot = Plot(data)
class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.main_frame = tk.Frame(self.root, bg='Slategray2')
        self.main_frame.pack(expand=True, fill='both')

        self.inner_frame = tk.Frame(self.main_frame, bg='Slategray1')
        self.inner_frame.pack(expand=True, fill='both', padx=10, pady=(10, 70))  

        self.top_bar = tk.Frame(self.inner_frame, bg='gray', height=15)
        self.top_bar.pack(fill='x')

        self.left_frame = tk.Frame(self.inner_frame, bg='Slategray1')
        self.left_frame.pack(side='left', expand=True, fill='both')

        self.right_frame = tk.Frame(self.inner_frame, bg='Slategray1')
        self.right_frame.pack(side='right', expand=True, fill='both')

        self.label_current_dataset = tk.Label(self.left_frame, background='Slategray1', text="Current Data Set", font=('Arial', 12, 'bold italic'), anchor='w', highlightthickness=0)
        self.label_current_dataset.pack(fill='x', padx=10, pady=(10, 5))

        self.label_count_of_rows = tk.Label(self.left_frame, background='Slategray1', text="Count of Rows", font=('Arial', 12, 'bold italic'), anchor='w', highlightthickness=0)
        self.label_count_of_rows.pack(fill='x', padx=10, pady=(5, 10))

        self.option_var = tk.StringVar(self.left_frame)
        self.option_menu = tk.OptionMenu(self.left_frame, self.option_var, ())
        self.option_menu.config(font=('Arial', 12), background='gray', foreground='white')
        self.option_menu.pack(fill='x', padx=10, pady=10)

        self.reset_button = tk.Button(self.left_frame, text="Reset", command=self.reset_option, width=25, height=2, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
        self.reset_button.pack(padx=10, pady=10, side='bottom')

        # Создание горизонтальной полосы прокрутки
        self.horizontal_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL)
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Создание Listbox с привязкой к горизонтальной полосе прокрутки
        self.listbox = tk.Listbox(self.right_frame, width=150, font=14, background='gray', foreground='white', xscrollcommand=self.horizontal_scrollbar.set)
        self.listbox.pack(expand=True, fill='both', padx=10, pady=10)

        # Привязка горизонтальной полосы прокрутки к Listbox
        self.horizontal_scrollbar.config(command=self.listbox.xview)

        self.buttons_frame = tk.Frame(self.main_frame, bg='Slategray2')  
        self.buttons_frame.pack(fill='x', pady=(0, 10)) 

        self.select_file_button = tk.Button(self.buttons_frame, text="SELECT FILE", command=lambda: self.select_file(self.main_frame), width=30, height=3, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
        self.select_file_button.pack(side='left', padx=(10, 5))

        self.create_graph_button = tk.Button(self.buttons_frame, text="CREATE GRAPH", command=lambda: self.create_graph(self.inner_frame), width=30, height=3, font=('Arial', 12, 'bold italic'), bg='gray', fg='white', bd=0, highlightthickness=0)
        self.create_graph_button.pack(side='right', padx=(5, 10))

        self.root.mainloop()

    def load_data(self):
        self.data = load_file_once()
        if self.data is not None:
            header = self.data.head().reset_index(drop=True)  
            self.update_data_frame(header)
            self.update_option_menu(header)  

    def select_file(self, data_frame):
        self.load_data()

    def create_graph(self, data_frame):
        if self.data is not None:
            filtered_data = plot.filter_data(self.data)  
            plot.make_3d_graph(*filtered_data)

    def update_data_frame(self, header):
        self.listbox.delete(0, tk.END)

        valid_columns = [column for column in header.columns if column.isidentifier()]

        header_string = " ".join(valid_columns)
        self.listbox.insert(tk.END, header_string)

        column_widths = [max(len(str(row[column])) for _, row in header.iterrows()) for column in valid_columns]

        for _, row in header.iterrows():
            row_string = "  ".join(f"{row[column]:<{width}}" for column, width in zip(valid_columns, column_widths))
            self.listbox.insert(tk.END, row_string)

    def update_option_menu(self, header=None):
        options = [column for column in header.columns if column.isidentifier()] if header is not None else []

        if options:
            self.option_var.set("")  # Сброс текущего значения
            self.option_menu['menu'].delete(0, 'end')  # Очистка старых вариантов

            for option in options:
                self.option_menu['menu'].add_command(label=option, command=tk._setit(self.option_var, option))
        else:
            self.option_var.set("No Options")  # Установка сообщения, когда нет вариантов для выбора
            self.option_menu['menu'].delete(0, 'end')  # Очистка старых вариантов

    def reset_option(self):
        selected_column = self.option_var.get()
        if selected_column in self.data.columns:
            self.data.drop(columns=[selected_column], inplace=True)
            updated_header = self.data.head().reset_index(drop=True)

            self.update_data_frame(updated_header)
            self.update_option_menu(updated_header)
            
            # Удаление выбранного элемента из listBox
            items = self.listbox.get(0, tk.END)
            try:
                index = items.index(selected_column)
                self.listbox.delete(index)
            except ValueError:
                pass  # Если столбец уже удален или его нет в listBox

            self.option_var.set("")  # Сброс выбранной опции в OptionMenu

def load_file_once():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename()
    if file_path:
        data = plot.load_file(file_path)
        return data  
    return None 

if __name__ == "__main__":
    Main()