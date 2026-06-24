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
