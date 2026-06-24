from algorithms import binary_search_plant, sort_beds_by_area
from entities.greenhouse import Greenhouse
from entities.plant import Plant
from utils import print_menu, show_catalog


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

    catalog = sorted(
        [
            Plant("Базилик", 14, 5, 22),
            Plant("Морковь", 60, 10, 18),
            Plant("Огурец", 30, 15, 26),
            Plant("Петрушка", 20, 7, 20),
            Plant("Перец", 50, 18, 27),
            Plant("Салат", 10, 8, 18),
            Plant("Томат", 45, 20, 25),
            Plant("Укроп", 15, 4, 19),
        ],
        key=lambda p: p.name,
    )

    gh.plant_on_bed(1, Plant("Огурец", 30, 15, 26))
    gh.plant_on_bed(2, Plant("Салат", 10, 8, 18))
    gh.plant_on_bed(3, Plant("Томат", 45, 20, 25))

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
                print(
                    f"  Найдено: {result.name} | {result.days_to_harvest} дн. "
                    f"| {result.water_per_day} л/день | {result.optimal_temp}C"
                )
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
                area = float(input("  Площадь (м/кв): "))
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
            print(
                f"\n  Завершение работы. Собрано урожаев: {len(gh.harvest_log)}. пока!"
            )
            break

        else:
            print("  Неизвестная команда")


if __name__ == "__main__":
    main()
