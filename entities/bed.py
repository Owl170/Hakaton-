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
