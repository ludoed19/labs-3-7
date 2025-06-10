#26 Формируется матрица F следующим образом: Скопировать в нее матрицу А и если сумма чисел по периметру области 1 больше, чем количество нулей по периметру области 4, то поменять симметрично области 1 и 3 местами, иначе 1 и 2 поменять местами несимметрично. 
# При этом матрица А не меняется. После чего вычисляется выражение:((К*AT)*А)-K*FT . Выводятся по мере формирования А, F и все матричные операции последовательно.
def read_matrix(filename):
    return [list(map(int, line.split())) for line in open(filename)]

def print_matrix(m, name):
    print(f"\n{name}:")
    for row in m:
        print(" ".join(f"{x:4}" for x in row))

def transpose(m):
    return [list(row) for row in zip(*m)]

def get_regions(n):
    # Возвращает списки координат областей 1, 2, 3, 4
    a1, a2, a3, a4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1:
                a1.append((i, j))
            elif i < j and i + j > n - 1:
                a2.append((i, j))
            elif i > j and i + j > n - 1:
                a3.append((i, j))
            elif i > j and i + j < n - 1:
                a4.append((i, j))
    return a1, a2, a3, a4

def get_perimeter(indices):
    # Возвращает координаты по “периметру” внутри области
    min_i = min(i for i, _ in indices)
    max_i = max(i for i, _ in indices)
    min_j = min(j for _, j in indices)
    max_j = max(j for _, j in indices)
    return [(i, j) for i, j in indices
            if i in (min_i, max_i) or j in (min_j, max_j)]

def build_F(A):
    n = len(A)
    # начинаем с копии A
    F = [row[:] for row in A]

    a1, a2, a3, a4 = get_regions(n)
    perim1 = get_perimeter(a1)
    perim4 = get_perimeter(a4)

    sum_perim1   = sum(A[i][j] for i, j in perim1)
    zeros_perim4 = sum(1 for i, j in perim4 if A[i][j] == 0)

    if sum_perim1 > zeros_perim4:
        # --- СИММЕТРИЧНЫЙ обмен областей 1 и 3 ---
        # для каждой точки (i,j) из области 1 берём зеркальную
        # точку (n-1-i, n-1-j) из области 3 и меняем их местами
        for (i, j) in a1:
            i3, j3 = n - 1 - i, n - 1 - j
            F[i][j], F[i3][j3] = F[i3][j3], F[i][j]
    else:
        # --- НЕСИММЕТРИЧНЫЙ обмен областей 1 и 2 ---
        # координаты области 2 проходим в обратном порядке
        for (i1, j1), (i2, j2) in zip(sorted(a1), reversed(sorted(a2))):
            F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]

    return F, sum_perim1, zeros_perim4

def compute_result(A, F, K):
    n = len(A)
    A_T = transpose(A)
    F_T = transpose(F)

    # (K*A^T)*A
    KA_T = [[K * A_T[i][j] for j in range(n)] for i in range(n)]
    left = [
        [sum(KA_T[i][k] * A[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]
    # K*F^T
    right = [[K * F_T[i][j] for j in range(n)] for i in range(n)]
    # разница
    return [
        [left[i][j] - right[i][j] for j in range(n)]
        for i in range(n)
    ]

if __name__ == "__main__":
    K = int(input("Введите K: "))
    A = read_matrix("matrix.txt")

    F, sum1, zeros4 = build_F(A)
    R = compute_result(A, F, K)

    print_matrix(A,   "Исходная матрица A")
    print(f"\nСумма по периметру области 1:   {sum1}")
    print(f"Число нулей по периметру области 4: {zeros4}")
    print_matrix(F,   "Матрица F после обмена")
    print_matrix(R,   "Результат ((K*A^T)*A) - K*F^T")
