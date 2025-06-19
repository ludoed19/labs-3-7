import math, timeit
import matplotlib.pyplot as plt

def sign(n):
    return 1 if n % 2 == 0 else -1

def F_recursive(n):
    if n < 2:
        return 1
    return sign(n) * (F_recursive(n - 1) / math.factorial(2 * n) - math.cos(F_recursive(n - 2) + 2))

def F_iterative(n):
    if n < 2:
        return 1
    f2, f1 = 1, 1
    fact = 1  # начнём с 1 и будем накапливать факториал 2*i
    for i in range(1, n + 1):
        # умножаем на два числа, чтобы получить (2*i)! постепенно
        fact *= (2 * i - 1)
        fact *= (2 * i)
        if i < 2:
            continue
        # вычисляем текущее значение
        cur = sign(i) * (f1 / fact - math.cos(f2 + 2))
        f2, f1 = f1, cur
    return f1

def main():
    res = []
    for n in range(21):
        tr = timeit.timeit(lambda: F_recursive(n), number=10)
        ti = timeit.timeit(lambda: F_iterative(n), number=10)
        res.append((n, tr, ti))

    print(f"{' n':>3}|{'Rec Time (s)':>12}|{'Iter Time (s)':>14}")
    print('-' * 37)
    for n, tr, ti in res:
        print(f"{n:3d}|{tr:12.6f}|{ti:14.6f}")

    xs = [r[0] for r in res]
    yr = [r[1] for r in res]
    yi = [r[2] for r in res]

    plt.figure(figsize=(8, 5))
    plt.plot(xs, yr, '--o', label='Рекурсивный метод')
    plt.plot(xs, yi,  '-o', label='Итеративный метод')
    plt.xlabel('n')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение времени вычисления F(n)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
