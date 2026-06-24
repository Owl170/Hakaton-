import random
from collections import deque



# клаассы 


class Plant:
    def __init__(self, name, days_to_harvest, water_per_day, optimal_temp):
        self.name = name
        self.days_to_harvest = days_to_harvest
        self.water_per_day = water_per_day
        self.optimal_temp = optimal_temp
        self.days_grown = 0.0
        self.stressed = False

    def clone(self):
        return Plant(self.name, self.days_to_harvest, self.water_per_day, self.optimal_temp)

    def grow(self, current_temp=None):
        if current_temp is not None and abs(current_temp - self.optimal_temp) > 5:
            self.stressed = True
            
        if self.stressed:
            self.days_grown += 0.5
        else:
            self.days_grown += 1

    def is_ready(self):
        return self.days_grown >= self.days_to_harvest

    def progress_bar(self):
        total = 10
        filled = int((self.days_grown / self.days_to_harvest) * total)
        filled = min(filled, total)
        bar = "1" * filled + "0" * (total - filled)
        pct = int((self.days_grown / self.days_to_harvest) * 100)
        pct = min(pct, 100)
        return f"[{bar}] {pct}%"

    def __str__(self):
        stress_mark = " стресс" if self.stressed else ""
        return f"{self.name} {self.progress_bar()} ({self.days_grown:g}/{self.days_to_harvest} дн.){stress_mark}"


class Bed:
    def __init__(self, bed_id, area):
        self.bed_id = bed_id
        self.area = area
        self.plant = None
        self.history = []  

    def plant_crop(self, plant):
        self.plant = plant

    def harvest(self):
        if self.plant is None:
            return None
        crop = self.plant
        self.history.append(crop.name)
        self.plant = None
        return crop

    def show_history(self):
        if not self.history:
            return "история пуста"
        return " -> ".join(self.history)

    def __str__(self):
        status = str(self.plant) if self.plant else "пусто"
        return f"Грядка #{self.bed_id} ({self.area} м²): {status}"


class Sensor:
    def __init__(self, sensor_id, sensor_type, bed_id):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.bed_id = bed_id
        self.value = 0.0
        self.history = []

    def read(self, value):
        self.value = round(value, 1)
        self.history.append(self.value)
        if len(self.history) > 5:
            self.history.pop(0)

    def simulate_reading(self):
        delta = random.uniform(-1.5, 1.5)
        self.read(self.value + delta)

    def __str__(self):
        trend = " ".join(str(v) for v in self.history[-3:]) if self.history else "—"
        return f"Датчик [{self.sensor_type}] грядка #{self.bed_id}: {self.value}  (последние: {trend})"


class Greenhouse:
    def __init__(self, name):
        self.name = name
        self.beds = {}
        self.sensors = {}
        self.task_queue = deque()
        self.day = 1
        self.water_tank = float('inf')
        self.harvest_log = []

    #  грядки
    def add_bed(self, bed_id, area):
        if bed_id in self.beds:
            print(f"  Грядка #{bed_id} уже существует")
            return
        self.beds[bed_id] = Bed(bed_id, area)
        print(f"   Грядка #{bed_id} добавлена ({area} м²)")

    def plant_on_bed(self, bed_id, plant):
        if bed_id not in self.beds:
            print("  Грядка не найдена")
            return False
        if self.beds[bed_id].plant:
            print("  Грядка уже занята — сначала уберите растение или дождитесь урожая")
            return False
        self.beds[bed_id].plant_crop(plant)
        print(f"   Посажено: {plant.name} на грядку #{bed_id}")
        return True

    # датчики

    def add_sensor(self, sensor_id, sensor_type, bed_id):
        if bed_id not in self.beds:
            print(f"  Грядка #{bed_id} не найдена — сначала добавьте грядку")
            return
        self.sensors[sensor_id] = Sensor(sensor_id, sensor_type, bed_id)
        print(f"   Датчик '{sensor_type}' установлен на грядку #{bed_id}")

    def update_sensor(self, sensor_id, value):
        if sensor_id not in self.sensors:
            print("  Датчик не найден")
            return
        self.sensors[sensor_id].read(value)
        print(f"   Датчик {sensor_id} обновлён: {value}")

    # задачи

    def add_task(self, task):
        if not task:
            print("  Задача не может быть пустой")
            return
        self.task_queue.append(task)
        print(f"   Задача добавлена (в очереди: {len(self.task_queue)})")

    #  симуляция дня 

    def simulate_day(self):
        print(f"\n{'='*55}")
        print(f"  ДЕНЬ {self.day}  —  {self.name}")
        print(f"{'='*55}")

        if self.task_queue:
            print("  [Задачи]")
            while self.task_queue:
                task = self.task_queue.popleft()
                print(f"     {task}")
        else:
            print("  [Задач нет]")

        for s in self.sensors.values():
            s.simulate_reading()





        temp_map = {s.bed_id: s.value for s in self.sensors.values() if s.sensor_type == "температура"}

        print("  [Полив и рост]")
        for bed in self.beds.values():
            if not bed.plant:
                continue
                
            water_needed = bed.plant.water_per_day
            bed.plant.grow(temp_map.get(bed.bed_id))
            temp = temp_map.get(bed.bed_id)
            temp_str = f", темп {temp}C" if temp else ""
            print(f"    Грядка #{bed.bed_id}: полито −{water_needed} л{temp_str}")

        ready = find_bed_with_ready_crop(self.beds)
        if ready:
            print("  [Сбор урожая]")
            for bed in ready:
                crop = bed.harvest()
                self.harvest_log.append((self.day, crop.name, bed.bed_id))
                print(f"     Собран: {crop.name} с грядки #{bed.bed_id}")

        print(f"  Вода: бесконечно")
        self.day += 1

    # вывод

    def show_status(self):
        print(f"\n{'─'*55}")
        print(f"  Теплица «{self.name}»  |  День {self.day}  |  Вода: бесконечно")
        print(f"{'─'*55}")
        print("  Грядки:")
        for bed in self.beds.values():
            print(f"    {bed}")
        print("  Датчики:")
        if self.sensors:
            for s in self.sensors.values():
                print(f"    {s}")
        else:
            print("    нет датчиков")

    def show_harvest_log(self):
        print("\n--- История урожаев ---")
        if not self.harvest_log:
            print("  Пусто — ждём первого урожая")
            return
        for day, crop, bed_id in self.harvest_log:
            print(f"  День {day}: {crop}  (грядка #{bed_id})")

    def show_bed_history(self, bed_id):
        if bed_id not in self.beds:
            print("  Грядка не найдена")
            return
        print(f"  История грядки #{bed_id}: {self.beds[bed_id].show_history()}")



# алгоритмы


def sort_beds_by_area(beds):
    return sorted(beds.values(), key=lambda b: b.area, reverse=True)


def find_bed_with_ready_crop(beds):
    return [b for b in beds.values() if b.plant and b.plant.is_ready()]


def binary_search_plant(catalog, target):
    target = target.lower()
    lo, hi = 0, len(catalog) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_name = catalog[mid].name.lower()
        if mid_name == target:
            return catalog[mid]
        elif mid_name < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None



# меню 

def print_menu():
    print("           АгроДом - меню         ")
    print("  1. Состояние теплицы            ")
    print("  2. Добавить задачу              ")
    print("  3. Посадить растение из каталога")
    print("  4. следующий день               ")
    print("  5. Журнал урожаев               ")
    print("  6. Грядки по площади            ")
    print("  7. Поиск по каталогу            ")
    print("  8. История грядки               ")
    print("  9. Добавить грядку              ")
    print(" 10. Обновить датчик              ")
    print("  0. Выход                        ")

def show_catalog(catalog):
    print("\n  Каталог культур:")
    for i, p in enumerate(catalog, 1):
        print(f"  {i}. {p.name:12} | {p.days_to_harvest} дн. | {p.water_per_day} л/день | оптим. {p.optimal_temp}C")


def main():
    print("  Запуск системы управления теплицей")

    gh = Greenhouse("АгроДом №1")
    gh.add_bed(1, 12)
    gh.add_bed(2, 8)
    gh.add_bed(3, 15)
    gh.add_sensor("t1", "температура", 1)
    gh.add_sensor("t2", "температура", 3)
    gh.add_sensor("h1", "влажность", 2)
    gh.sensors["t1"].read(24.5)
    gh.sensors["t2"].read(26.0)
    gh.sensors["h1"].read(65.0)

    catalog = sorted([
        Plant("Базилик",  14,  5, 22),
        Plant("Морковь",  60, 10, 18),
        Plant("Огурец",   30, 15, 26),
        Plant("Петрушка", 20,  7, 20),
        Plant("Перец",    50, 18, 27),
        Plant("Салат",    10,  8, 18),
        Plant("Томат",    45, 20, 25),
        Plant("Укроп",    15,  4, 19),
    ], key=lambda p: p.name)

    gh.plant_on_bed(1, Plant("Огурец",  30, 15, 26))
    gh.plant_on_bed(2, Plant("Салат",   10,  8, 18))
    gh.plant_on_bed(3, Plant("Томат",   45, 20, 25))

    while True:
        print_menu()
        choice = input("Выберите: ").strip()

        if choice == "1":
            gh.show_status()

        elif choice == "2":
            task = input("  Введите задачу: ").strip()
            gh.add_task(task)

        elif choice == "3":
            show_catalog(catalog)
            try:
                idx = int(input("  Номер из каталога: ")) - 1
                if not (0 <= idx < len(catalog)):
                    print("  Нет такого номера")
                    continue
                bed_id = int(input("  Номер грядки: "))
                gh.plant_on_bed(bed_id, catalog[idx].clone())
            except ValueError:
                print("  Ошибка: введите число")

        elif choice == "4":
            gh.simulate_day()

        elif choice == "5":
            gh.show_harvest_log()

        elif choice == "6":
            print("\n  Грядки по убыванию площади:")
            for bed in sort_beds_by_area(gh.beds):
                print(f"    {bed}")

        elif choice == "7":
            target = input("  Введите название (без учета регистра): ").strip()
            result = binary_search_plant(catalog, target)
            if result:
                print(f"  Найдено: {result.name} | {result.days_to_harvest} дн. "
                      f"| {result.water_per_day} л/день | {result.optimal_temp}C")
            else:
                print("  Не найдено. Доступные культуры:")
                show_catalog(catalog)

        elif choice == "8":
            try:
                bed_id = int(input("  Номер грядки: "))
                gh.show_bed_history(bed_id)
            except ValueError:
                print("  Ошибка ввода")

        elif choice == "9":
            try:
                bed_id = int(input("  ID новой грядки: "))
                area   = float(input("  Площадь (м/кв): "))
                if area <= 0:
                    print("  Площадь должна быть > 0")
                else:
                    gh.add_bed(bed_id, area)
            except ValueError:
                print("  Ошибка ввода")

        elif choice == "10":
            if not gh.sensors:
                print("  Датчиков нет")
            else:
                print("  Доступные датчики:", ", ".join(gh.sensors.keys()))
                sid = input("  ID датчика: ").strip()
                if sid not in gh.sensors:
                    print("  Такого датчика нет")
                    continue
                try:
                    val = float(input("  Новое значение: "))
                    # Защита от смешариков из ромашковой долины 
                    if -50 <= val <= 150:
                        gh.update_sensor(sid, val)
                    else:
                        print("  Ошибка: значение выходит за рамки здравого смысла!")
                except ValueError:
                    print("  Ошибка ввода")

        elif choice == "0":
            print(f"\n  Завершение работы. Собрано урожаев: {len(gh.harvest_log)}. пока!")
            break

        else:
            print("  Неизвестная команда")


if __name__ == "__main__":
    main()