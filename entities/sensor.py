import random


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
        trend = " ".join(str(v) for v in self.history[-3:]) if self.history else "-"
        return f"Датчик [{self.sensor_type}] грядка #{self.bed_id}: {self.value}  (последние: {trend})"
