from pynput import keyboard
from clouds import Clouds
from map import Map
import time
import os
import json
from helicopter import Helicopter as Helico

# Конфигурация игры
TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 50
MAP_W, MAP_H = 20, 20
SAVE_FILE = "save.json"

# Игровые объекты
field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
tick = 1
# Управление
MOVES = {
    'w': (-1, 0),  # вверх
    'd': (0, 1),   # вправо
    's': (1, 0),   # вниз
    'a': (0, -1),  # влево
}

def save_game():
    """Сохраняет текущее состояние игры"""
    data = {
        "helico": helico.export_data(),
        "clouds": clouds.export_data(),
        "field": field.export_data(),
        "tick": tick
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print(f"Игра сохранена в {SAVE_FILE}")

def load_game():
    """Загружает сохраненную игру"""
    global helico, tick, field, clouds
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        
        helico.import_data(data["helico"])
        clouds.import_data(data["clouds"])
        field.import_data(data["field"])
        tick = data["tick"]
        print(f"Игра загружена из {SAVE_FILE}")
    except FileNotFoundError:
        print("Файл сохранения не найден! Начинаем новую игру.")
    except Exception as e:
        print(f"Ошибка загрузки: {str(e)}. Начинаем новую игру.")

def on_key_release(key):
    """Обработчик нажатий клавиш"""
    global helico, tick
    try:
        c = key.char.lower()
        
        # Движение вертолета
        if c in MOVES:
            dx, dy = MOVES[c]
            helico.move(dx, dy)
        
        # Сохранение/загрузка
        elif c == 'f':
            save_game()
        elif c == 'g':
            load_game()
            
    except AttributeError:
        pass

# Запуск обработчика клавиш
listener = keyboard.Listener(on_release=on_key_release)
listener.start()

# Главный игровой цикл
try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Обновление игрового состояния
        field.process_helicopter(helico, clouds)
        helico.print_stats()
        print("WELCOME TO HELL")
        field.print_map(helico, clouds)
        print(f"TICK: {tick}")
        print("Управление: WASD - движение, F - сохранить, G - загрузить")
        
        # Обновление игровых объектов
        if tick % TREE_UPDATE == 0:
            field.generate_tree()
        if tick % FIRE_UPDATE == 0:
            field.update_fires()
        if tick % CLOUDS_UPDATE == 0:
            clouds.update()
        
        tick += 1
        time.sleep(TICK_SLEEP)

except KeyboardInterrupt:
    print("\nИгра завершена")
except Exception as e:
    print(f"Критическая ошибка: {str(e)}")
    time.sleep(5)