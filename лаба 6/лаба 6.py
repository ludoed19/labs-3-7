# Задана рекуррентная функция. 
# Область определения функции – натуральные числа. 
# Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
# Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
# Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде отчета по лабораторной работе.
# F(0) = F(1) = 1, F(n) = (-1)n*(F(n–1) /(2n)!-cos(F(n-2)+2)), при n > 1
import timeit
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial, cos

# Рекурсивная реализация
def rec_F(n):
    if n == 0 or n == 1:
        return 1
    sign = -1 if n % 2 else 1
    return sign * (rec_F(n-1) / factorial(2*n) - cos(rec_F(n-2) + 2)

# Итерационная реализация с оптимизацией
def iter_F(n):
    if n == 0 or n == 1:
        return 1
    
    # Инициализация значений для n=0 и n=1
    F = [1, 1]
    fact = 1  # Будем накапливать факториал (2n)! итерационно
    
    for k in range(2, n+1):
        # Вычисляем (2k)! = (2(k-1))! * (2k-1)*(2k)
        fact *= (2*k-1) * (2*k)
        sign = -1 if k % 2 else 1
        next_val = sign * (F[-1] / fact - cos(F[-2] + 2))
        F.append(next_val)
    
    return F[-1]

if __name__ == '__main__':
    # Определяем диапазон n, который мы можем вычислить за разумное время
    max_n_rec = 15  # Максимальное n для рекурсивного метода (ограничено стеком и временем)
    max_n_iter = 30  # Максимальное n для итерационного метода
    
    ns_rec = list(range(max_n_rec + 1))
    ns_iter = list(range(max_n_iter + 1))
    
    # Измеряем время для рекурсивного метода
    results_rec = []
    for n in ns_rec:
        try:
            value = rec_F(n)
            time = timeit.timeit(lambda: rec_F(n), number=10)
            results_rec.append((n, value, time))
        except:
            results_rec.append((n, None, None))
            break
    
    # Измеряем время для итерационного метода
    results_iter = []
    for n in ns_iter:
        try:
            value = iter_F(n)
            time = timeit.timeit(lambda: iter_F(n), number=10)
            results_iter.append((n, value, time))
        except:
            results_iter.append((n, None, None))
            break
    
    # Создаем DataFrame для результатов
    df_rec = pd.DataFrame(results_rec, columns=['n', 'Rec_F(n)', 'Rec_time (s)'])
    df_iter = pd.DataFrame(results_iter, columns=['n', 'Iter_F(n)', 'Iter_time (s)'])
    
    # Объединяем результаты в одну таблицу
    df = pd.merge(df_rec, df_iter, on='n', how='outer')
    print(df.to_string(index=False))
    
    # Строим графики
    plt.figure(figsize=(12, 6))
    
    # График значений
    plt.subplot(1, 2, 1)
    plt.plot(df['n'], df['Rec_F(n)'], 'o-', label='Рекурсия')
    plt.plot(df['n'], df['Iter_F(n)'], 's-', label='Итерация')
    plt.xlabel('n')
    plt.ylabel('F(n)')
    plt.title('Значения функции')
    plt.legend()
    plt.grid(True)
    
    # График времени
    plt.subplot(1, 2, 2)
    plt.plot(df['n'], df['Rec_time (s)'], 'o-', label='Рекурсия')
    plt.plot(df['n'], df['Iter_time (s)'], 's-', label='Итерация')
    plt.xlabel('n')
    plt.ylabel('Время (сек)')
    plt.title('Время вычисления')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
