import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
from scipy.sparse import csr_matrix

# Implementación de representación CSR desde cero
class SparseMatrixCSR:
    def __init__(self, data, row_indices, col_indices, shape):
        self.data = data
        self.row_indices = row_indices
        self.col_indices = col_indices
        self.shape = shape

    @staticmethod
    def from_dense(dense_matrix):
        data = []
        row_indices = []
        col_indices = []
        for i, row in enumerate(dense_matrix):
            for j, val in enumerate(row):
                if val != 0:
                    data.append(val)
                    row_indices.append(i)
                    col_indices.append(j)
        return SparseMatrixCSR(data, row_indices, col_indices, dense_matrix.shape)

    def to_dense(self):
        dense_matrix = np.zeros(self.shape)
        for data, row, col in zip(self.data, self.row_indices, self.col_indices):
            dense_matrix[row, col] = data
        return dense_matrix

    def multiply(self, other):
        result = np.zeros(self.shape)
        for i, j, v in zip(self.row_indices, self.col_indices, self.data):
            for k in range(other.shape[1]):
                result[i, k] += v * other[j, k]
        return result

# Generar una matriz dispersa 30x30
def generar_matriz_sparse(size=30, density=0.1):
    dense_matrix = np.random.choice([0, 1], size=(size, size), p=[1-density, density])
    return dense_matrix

# Función para medir tiempos y realizar comparación
def comparar_multiplicacion(matriz_a, matriz_b):
    # Implementación de CSR desde cero
    inicio_manual = time.time_ns()
    matriz_sparse_manual = SparseMatrixCSR.from_dense(matriz_a)
    resultado_manual = matriz_sparse_manual.multiply(matriz_b)
    tiempo_manual = time.time_ns() - inicio_manual

    # Implementación con scipy.sparse
    inicio_scipy = time.time_ns()
    matriz_sparse_scipy = csr_matrix(matriz_a)
    resultado_scipy = matriz_sparse_scipy.dot(matriz_b)
    tiempo_scipy = time.time_ns() - inicio_scipy

    return tiempo_manual, tiempo_scipy, resultado_manual, resultado_scipy

# Mostrar tabla de comparación en la interfaz
def mostrar_resultado(matriz_a, matriz_b):
    tiempo_manual, tiempo_scipy, _, _ = comparar_multiplicacion(matriz_a, matriz_b)
    
    # Crear ventana para mostrar los resultados
    window_result = tk.Toplevel()
    window_result.title("Comparación de tiempos de ejecución")

    # Etiqueta indicando el método de representación usado
    tk.Label(window_result, text="Método de representación: CSR (Compressed Sparse Row)").pack()

    # Tabla de resultados
    cols = ('Método', 'Tiempo (ns)')
    table = ttk.Treeview(window_result, columns=cols, show='headings')
    
    for col in cols:
        table.heading(col, text=col)

    # Insertar filas en la tabla
    table.insert("", "end", values=("CSR Manual", tiempo_manual))
    table.insert("", "end", values=("scipy.sparse", tiempo_scipy))

    table.pack()

# Ventana para la opción de matrices sparse
def ventana_opcion2():
    window = tk.Toplevel()
    window.title("Representación de Matriz Sparse")

    # Crear matrices sparse de 30x30
    matriz_a = generar_matriz_sparse(30)
    matriz_b = generar_matriz_sparse(30)

    # Botón para realizar la comparación
    tk.Button(window, text="Comparar tiempos de ejecución", 
              command=lambda: mostrar_resultado(matriz_a, matriz_b)).pack(pady=10)

    # Mostrar las matrices generadas en la interfaz
    tk.Label(window, text="Matriz A (30x30):").pack()
    matriz_a_str = '\n'.join([' '.join(map(str, row)) for row in matriz_a])
    tk.Label(window, text=matriz_a_str).pack()

    tk.Label(window, text="Matriz B (30x30):").pack()
    matriz_b_str = '\n'.join([' '.join(map(str, row)) for row in matriz_b])
    tk.Label(window, text=matriz_b_str).pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Matrices Sparse")
    ventana_opcion2()
    root.mainloop()
