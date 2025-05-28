# Вариант 26. Вводятся К целых чисел. Составьте все возможные различные правильные дроби из этих чисел.
import timeit
from itertools import permutations
from math import prod

def get_leaves(edges, K):
    all_nodes = set(range(K))
    parents = set(u for u, v in edges)
    leaves = list(all_nodes - parents)
    return leaves

def algorithmic_method(K):
    def generate(arr, l, r, result):
        if l == r:
            result.append(arr[:])
            return
        for i in range(l, r+1):
            arr[l], arr[i] = arr[i], arr[l]
            generate(arr, l+1, r, result)
            arr[l], arr[i] = arr[i], arr[l]
    arr = list(range(1, K+1))
    result = []
    generate(arr, 0, K-1, result)
    return result

def python_method(K):
    return [list(p) for p in permutations(range(1, K+1))]

def optimized_method(labelings, leaves, root_idx):
    # Ограничение: корень = K (максимальное число)
    filtered = [lbl for lbl in labelings if lbl[root_idx] == max(lbl)]
    if not filtered:
        return []
    # Доп условие: последний лист должен быть четным
    last_leaf_idx = leaves[-1]
    filtered = [lbl for lbl in filtered if lbl[last_leaf_idx] % 2 == 0]
    if not filtered:
        return []
    # Целевая функция: максимизируем произведение значений на листьях
    max_product = max(prod(lbl[l] for l in leaves) for lbl in filtered)
    return [lbl for lbl in filtered if prod(lbl[l] for l in leaves) == max_product]

if __name__ == '__main__':
    K = 8
    edges = [(0,1), (0,2), (2,3)]  # пример дерева
    root_idx = 0
    leaves = get_leaves(edges, K)
    print("Индексы листьев дерева:", leaves)

    t_alg = timeit.timeit(lambda: algorithmic_method(K), number=1)
    alg = algorithmic_method(K)
    print(f"\nАлгоритмический способ: {len(alg)} вариантов, время: {t_alg:.4f}s")

    t_py = timeit.timeit(lambda: python_method(K), number=1)
    py = python_method(K)
    print(f"Способ через permutations: {len(py)} вариантов, время: {t_py:.4f}s")

    optimal = optimized_method(py, leaves, root_idx)
    if not optimal:
        print("\nОптимальных вариантов не найдено с заданными условиями.")
    else:
        print("\nПервые 10 оптимальных разметок (максимальное произведение на листьях, последний лист чётный):")
        for arr in optimal[:10]:
            print(arr, "→ листья:", [arr[l] for l in leaves])
        print(f"\nВсего оптимальных разметок: {len(optimal)}")
        print("Максимальное произведение на листьях:", 
              prod(optimal[0][l] for l in leaves))
