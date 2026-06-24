def print_menu():
    print("           АгроДом - меню         ")
    print("  1. Состояние теплицы            ")
    print("  2. Добавить задачу              ")
    print("  3. Посадить растение из каталога")
    print("  4. Следующий день               ")
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
        print(
            f"  {i}. {p.name:12} | {p.days_to_harvest} дн. | {p.water_per_day} л/день | оптим. {p.optimal_temp}C"
        )
