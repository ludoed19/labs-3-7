import math
import timeit
import pandas as pd
import matplotlib.pyplot as plt

def sign(n):
    return 1 if n % 2 == 0 else -1

def rec_F(n, fact_cache={0: 1, 1: 1}):
    if n == 0 or n == 1:
        return 1
    # Вычисляем факториалы последовательно до 2*n
    max_fact = max(fact_cache.keys())
    for num in range(max_fact + 1, 2 * n + 1):
        fact_cache[num] = fact_cache[num - 1] * num

    return sign(n) * (rec_F(n - 1, fact_cache) / fact_cache[2 * n] - math.cos(rec_F(n - 2, fact_cache) + 2))

def iter_F(n):
    if n == 0 or n == 1:
        return 1
    fact_cache = {0: 1, 1: 1}
    max_fact = 1
    values = [1, 1]
    for i in range(2, n + 1):
        # Последовательно вычисляем факториалы от max_fact + 1 до 2*i
        for num in range(max_fact + 1, 2 * i + 1):
            fact_cache[num] = fact_cache[num - 1] * num
        max_fact = 2 * i

        val = sign(i) * (values[i - 1] / fact_cache[2 * i] - math.cos(values[i - 2] + 2))
        values.append(val)
    return values[n]

if __name__ == '__main__':
    ns = list(range(0, 21))
    results = []

    for n in ns:
        t_rec = timeit.timeit(lambda: rec_F(n), number=10)
        t_it = timeit.timeit(lambda: iter_F(n), number=10)
        results.append((n, t_rec, t_it))

    df = pd.DataFrame(results, columns=['n', 'Recursive Time (s)', 'Iterative Time (s)'])
    print(df.to_string(index=False))

    plt.figure(figsize=(8, 5))
    plt.plot(df['n'], df['Recursive Time (s)'], '--o', label='Рекурсивный метод')
    plt.plot(df['n'], df['Iterative Time (s)'], '-o', label='Итеративный метод')
    plt.xlabel('n')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение времени вычисления F(n)')
    plt.legend()
    plt.grid(True)
    plt.show()
