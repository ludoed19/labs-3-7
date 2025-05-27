import numpy as np
import matplotlib.pyplot as plt

def load_matrix():
    A = np.loadtxt("matrix_data.txt", dtype=int)
    if A.shape[0] != A.shape[1]:
        exit("Матрица должна быть квадратной")
    return A

def build_F(A):
    F = A.copy()
    n = A.shape[0] // 2
    E = A[:n, :n]
    B = A[:n, n:]
    C = A[n:, n:]

    # В C: считаем количество нулей в нечётных столбцах
    zeros_C_odd_cols = np.sum((C[:, 1::2] == 0))
    # В C: произведение чисел по периметру
    perim = np.concatenate([C[0, :], C[-1, :], C[1:-1, 0], C[1:-1, -1]])
    prod_perim = np.prod(perim) if perim.size else 0

    print(f"\nНулей в нечётных столбцах C: {zeros_C_odd_cols}")
    print(f"Произведение чисел по периметру C: {prod_perim}")

    if zeros_C_odd_cols > prod_perim:
        # B и C меняем симметрично (относительно вертикальной оси внутри блока)
        F[:n, n:], F[n:, n:] = np.fliplr(C), np.fliplr(B)
        print("B и C поменялись симметрично")
    else:
        # B и E меняем нессиметрично (поэлементно)
        tmp = B.copy()
        F[:n, n:], F[:n, :n] = E, tmp
        print("B и E поменялись местами нессиметрично")
    return F

def compute_result(A, F, K):
    detA = np.linalg.det(A)
    diagF = np.trace(F)
    print(f"\nОпределитель A: {detA:.2f}")
    print(f"Сумма диагональных элементов F: {diagF:.2f}")

    if detA > diagF:
        res = A @ A.T - K * F
        print("Результат: A * A^T - K * F")
    else:
        G = np.tril(A)
        F_inv = np.linalg.inv(F)
        res = (A + G - F_inv) * K
        print("Результат: (A + G - F^-1) * K")
    return res

def plot_graphs(F):
    plt.figure(figsize=(16,4))
    plt.subplot(1,3,1)
    plt.imshow(F, cmap='viridis')
    plt.title("F как изображение"); plt.colorbar()
    plt.subplot(1,3,2)
    plt.plot(np.sum(F, axis=1), marker='o')
    plt.title("Сумма по строкам")
    plt.grid(True)
    plt.subplot(1,3,3)
    plt.hist(F.flatten(), bins=10)
    plt.title("Гистограмма элементов F")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    K = int(input("Введите K: "))
    A = load_matrix()
    print("\nA:\n", A)
    F = build_F(A)
    print("\nF:\n", F)
    R = compute_result(A, F, K)
    print("\nРезультат:\n", R)
    plot_graphs(F)

main()
