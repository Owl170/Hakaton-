from collections import deque

from algorithms import find_bed_with_ready_crop
from entities.bed import Bed
from entities.sensor import Sensor


class Greenhouse:
    def __init__(self, name):
        self.name = name
        self.beds = {}
        self.sensors = {}
        self.task_queue = deque()
        self.day = 1
        self.water_tank = float("inf")
        self.harvest_log = []

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
            print("  Грядка уже занята : сначала уберите растение или дождитесь урожая")
            return False

        self.beds[bed_id].plant_crop(plant)
        print(f"   Посажено: {plant.name} на грядку #{bed_id}")

        return True

    def add_sensor(self, sensor_id, sensor_type, bed_id):
        if bed_id not in self.beds:
            print(f"  Грядка #{bed_id} не найдена : сначала добавьте грядку")
            return

        self.sensors[sensor_id] = Sensor(sensor_id, sensor_type, bed_id)
        print(f"   Датчик '{sensor_type}' установлен на грядку #{bed_id}")

    def update_sensor(self, sensor_id, value):
        if sensor_id not in self.sensors:
            print("  Датчик не найден")
            return

        self.sensors[sensor_id].read(value)
        print(f"   Датчик {sensor_id} обновлён: {value}")

    def add_task(self, task):
        if not task:
            print("  Задача не может быть пустой")
            return

        self.task_queue.append(task)
        print(f"   Задача добавлена (в очереди: {len(self.task_queue)})")

    def simulate_day(self):
        print(f"\n{'=' * 55}")
        print(f"  ДЕНЬ {self.day}  :  {self.name}")
        print(f"{'=' * 55}")

        if self.task_queue:
            print("  [Задачи]")
            while self.task_queue:
                task = self.task_queue.popleft()
                print(f"     {task}")
        else:
            print("  [Задач нет]")

        for s in self.sensors.values():
            s.simulate_reading()

        temp_map = {
            s.bed_id: s.value
            for s in self.sensors.values()
            if s.sensor_type == "температура"
        }

        print("  [Полив и рост]")
        for bed in self.beds.values():
            if not bed.plant:
                continue

            water_needed = bed.plant.water_per_day
            bed.plant.grow(temp_map.get(bed.bed_id))
            temp = temp_map.get(bed.bed_id)
            temp_str = f", темп {temp}C" if temp else ""
            print(f"    Грядка #{bed.bed_id}: полито -{water_needed} л{temp_str}")

        ready = find_bed_with_ready_crop(self.beds)
        if ready:
            print("  [Сбор урожая]")
            for bed in ready:
                crop = bed.harvest()
                self.harvest_log.append((self.day, crop.name, bed.bed_id))
                print(f"     Собран: {crop.name} с грядки #{bed.bed_id}")

        print("  Вода: бесконечно")
        self.day += 1

    def show_status(self):
        print(f"\n{'─' * 55}")
        print(f"  Теплица '{self.name}'  |  День {self.day}  |  Вода: бесконечно")
        print(f"{'─' * 55}")
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
            print("  Пусто: ждём первого урожая")
            return

        for day, crop, bed_id in self.harvest_log:
            print(f"  День {day}: {crop}  (грядка #{bed_id})")

    def show_bed_history(self, bed_id):
        if bed_id not in self.beds:
            print("  Грядка не найдена")
            return

        print(f"  История грядки #{bed_id}: {self.beds[bed_id].show_history()}")
