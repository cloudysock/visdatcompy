import os
import time
import sys
from colorama import Fore, Style, init

init()

__all__ = ["get_time", "color_print", "scan_directory"]

colors = {
    "none": "",
    "status": Fore.LIGHTMAGENTA_EX,
    "done": Fore.GREEN,
    "fail": Fore.RED,
    "warning": Fore.YELLOW,
    "log": Fore.LIGHTBLACK_EX,
    "create": Fore.CYAN,
}  # Цвета текста

style = Style.BRIGHT
reset = Style.RESET_ALL

stamps = {
    "none": "",
    "status": "[%] ",
    "done": "[V] ",
    "fail": "[X] ",
    "warning": "[!] ",
    "log": "[$] ",
    "create": "[+] ",
}  # Штампы вывода

images = []

# ==================================================================================================================================
# |                                                            UTILS                                                               |
# ==================================================================================================================================


def get_time(func) -> None:
    """
    Декоратор для замера времени выполнения функции.

    Parameters:
        - func (function): функция, время выполнения которой требуется замерить

    Returns:
        - None
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time() - start_time

        color_print("log", "log", f"Время выполнения: {end_time}", True)

        return result

    return wrapper


# ==================================================================================================================================


def color_print(stamp: str, color: str, message: str, newline: bool = True) -> None:
    """
    Функция для красивого вывода в консоль.

    Parameters:
        - stamp (str): штамп для определения вида сообщения
        - color (str): цвет текста сообщения
        - message (str): текст сообщения
        - newline (bool): флаг, определяющий, нужно ли добавлять переход на новую строку

    Returns:
        - None

    Stamps:
        - "none": пустой штамп
        - "status": [%]
        - "done": [V]
        - "fail": [X]
        - "warning": [!]
        - "log": [$]
        - "create": [+]

    Colors:
        - "none": обычный белый цвет
        - "status": светло-пурпурный цвет
        - "done": зеленый цвет
        - "fail": красный цвет
        - "warning": желтый цвет
        - "log": светло-черный цвет
        - "create": голубой цвет

    Libraries:
        - colorama, установка: "pip install colorama"
    """

    to_new_line = "\n" if newline else " "

    sys.stdout.write(
        f"{to_new_line}{style}{colors[color]}{stamps[stamp]}{message}{reset}"
    )


# ==================================================================================================================================


def scan_directory(dataset_path: str, echo: bool = False) -> list[str]:
    """
    Функция для сканирования директории и сохранения путей изображений.

    Parameters:
        - dataset_path (str): путь к директории с изображениями

    Returns:
        - list[str]: список путей к изображениям
    """

    image_paths = []

    try:
        for address, _, files in os.walk(dataset_path):
            for name in files:
                image_paths.append((address, name))

                if echo:
                    color_print("log", "log", f"{address} - - - {name}")

    except Exception as e:
        color_print("fail", "fail", f"Ошибка сканирования директории: {e}")

    return image_paths


# ==================================================================================================================================


# Проверка на скорость выполнения функции для сканирования директории
if __name__ == "__main__":
    print(get_time(scan_directory)("dataset"))
