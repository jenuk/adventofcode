from .type_hints import C


def median_of_three(x: list[C]) -> C:
    if x[0] < x[1]:
        if x[1] < x[2]:
            return x[1]
        elif x[0] < x[2]:
            return x[2]
        else:
            return x[0]
    else:
        if x[0] < x[2]:
            return x[0]
        elif x[1] < x[2]:
            return x[2]
        else:
            return x[1]


def quickselect(elements: list[C], nth: int) -> C:
    def partition(left, right):
        if right - left > 5:
            subselect = [
                (elements[left], left),
                (elements[(left + right) // 2], (left + right) // 2),
                (elements[right], right),
            ]
            pivot, pivot_idx = median_of_three(subselect)
        else:
            pivot_idx = (left + right) // 2
            pivot = elements[pivot_idx]
        elements[pivot_idx], elements[right] = elements[right], elements[pivot_idx]
        store = left
        for i in range(left, right):
            if elements[i] < pivot:
                elements[i], elements[store] = elements[store], elements[i]
                store += 1
        elements[right], elements[store] = elements[store], elements[right]
        return store

    left = 0
    right = len(elements) - 1
    while (pivot_idx := partition(left, right)) != nth:
        if pivot_idx < nth:
            left = pivot_idx + 1
        else:
            right = pivot_idx - 1

    return elements[nth]
