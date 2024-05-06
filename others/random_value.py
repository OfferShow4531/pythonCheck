import random
import string

def get_options_value(option):
    if option == "xmin" or option == "xmax" or option == "ymax" or option == "ymin":
        return round(random.uniform(0.0, 1.0), 2)
    elif option == "c":
        return round(random.uniform(0.0, 2.0), 2)
    elif option == "cmap":
        return random.choice(["gray", "pink", "blue", "red", "green", "purple"])  # Выбор случайного цвета
    elif option == "clblabel" or option == "clbwidth" or option == "scalebarsize" or option == "axislabelsize" or option == "ticklabelsize":
        return random.randint(0, 10)  # Случайное целое число от 0 до 10
    elif option == "azim" or option == "elev":
        return random.randint(0, 10)  # Случайное целое число от 0 до 30
    else:
        return None  # В случае неизвестной опции возвращаем None