import tkinter as tk
from tkinter import scrolledtext, messagebox
from itertools import permutations
from math import prod
import time

def get_leaves(edges, K):
    all_nodes = set(range(K))
    parents = set(u for u, v in edges)
    leaves = list(all_nodes - parents)
    return leaves

def python_method(K):
    # Генерация всех перестановок чисел 1..K
    return [list(p) for p in permutations(range(1, K+1))]

def optimized_method(labelings, leaves, root_idx):
    filtered = [lbl for lbl in labelings if lbl[root_idx] == max(lbl)]
    if not filtered:
        return []
    last_leaf_idx = leaves[-1]
    filtered = [lbl for lbl in filtered if lbl[last_leaf_idx] % 2 == 0]
    if not filtered:
        return []
    max_product = max(prod(lbl[l] for l in leaves) for lbl in filtered)
    return [lbl for lbl in filtered if prod(lbl[l] for l in leaves) == max_product]

class App:
    def __init__(self, root):
        self.root = root
        root.title("Оптимизация разметки дерева")

        # Ввод K
        tk.Label(root, text="Введите число вершин K:").grid(row=0, column=0, sticky="w")
        self.entry_k = tk.Entry(root, width=10)
        self.entry_k.grid(row=0, column=1, sticky="w")

        # Кнопка запуска
        self.btn_run = tk.Button(root, text="Запустить", command=self.run)
        self.btn_run.grid(row=0, column=2, padx=10)

        # Окно вывода с прокруткой
        self.output = scrolledtext.ScrolledText(root, width=90, height=30)
        self.output.grid(row=1, column=0, columnspan=3, pady=10)

        # Текстовое поле (просто пример, можно использовать для подсказок)
        tk.Label(root, text="Информация:").grid(row=2, column=0, sticky="w")
        self.info_text = tk.Text(root, height=3, width=90)
        self.info_text.grid(row=3, column=0, columnspan=3, pady=5)
        self.info_text.insert(tk.END, "Программа генерирует перестановки для разметки дерева.\n"
                                     "Оптимизация: корень = max число, последний лист четный,\n"
                                     "максимизируется произведение значений на листьях.")

    def run(self):
        self.output.delete('1.0', tk.END)
        try:
            K = int(self.entry_k.get())
            if K < 2:
                messagebox.showerror("Ошибка", "K должно быть не меньше 2")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число K")
            return

        # Пример ребер для K вершин (звезда + пары)
        edges = [(0,1), (0,2), (0,3), (1,4), (1,5), (2,6), (2,7)]
        if K < 8:
            # Урезаем ребра под K, чтобы индексы не выходили за границы
            edges = [(u,v) for u,v in edges if u < K and v < K]

        root_idx = 0
        leaves = get_leaves(edges, K)
        self.output.insert(tk.END, f"Индексы листьев: {leaves}\n\n")

        self.output.insert(tk.END, "Генерация перестановок...\n")
        start_time = time.time()
        permutations_list = python_method(K)
        elapsed = time.time() - start_time
        self.output.insert(tk.END, f"Всего перестановок: {len(permutations_list)}\n")
        self.output.insert(tk.END, f"Время генерации: {elapsed:.2f} сек\n\n")

        self.output.insert(tk.END, "Выгрузка первых 10 перестановок:\n")
        for p in permutations_list[:10]:
            self.output.insert(tk.END, f"{p}\n")

        self.output.insert(tk.END, "\nЗапуск оптимизации...\n")
        start_time = time.time()
        optimal = optimized_method(permutations_list, leaves, root_idx)
        elapsed = time.time() - start_time

        if not optimal:
            self.output.insert(tk.END, "Оптимальных вариантов не найдено с заданными условиями.\n")
            return

        self.output.insert(tk.END, f"Найдено оптимальных вариантов: {len(optimal)}\n")
        self.output.insert(tk.END, f"Время оптимизации: {elapsed:.2f} сек\n")
        self.output.insert(tk.END, "Первые 10 оптимальных вариантов:\n")
        for arr in optimal[:10]:
            leaf_vals = [arr[l] for l in leaves]
            self.output.insert(tk.END, f"{arr} → листья: {leaf_vals}, произведение: {prod(leaf_vals)}\n")

        best = optimal[0]
        leaf_vals = [best[l] for l in leaves]
        self.output.insert(tk.END, f"\nПример оптимального варианта:\n{best} → листья: {leaf_vals}, произведение: {prod(leaf_vals)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
