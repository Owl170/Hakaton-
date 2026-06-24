class Plant:
    def __init__(self, name, days_to_harvest, water_per_day, optimal_temp):
        self.name = name
        self.days_to_harvest = days_to_harvest
        self.water_per_day = water_per_day
        self.optimal_temp = optimal_temp
        self.days_grown = 0.0
        self.stressed = False

    def clone(self):
        return Plant(
            self.name, self.days_to_harvest, self.water_per_day, self.optimal_temp
        )

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
