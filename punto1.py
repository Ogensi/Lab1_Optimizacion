import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la función de costo f(x, y) = x^2 + y^2
def funcion_costo(x, y):
    return x**2 + y**2

# Función para graficar la región factible
def restricciones_graficas(ax, c1=4):
    # Restricciones: x + y <= c1, x >= 0, y >= 0
    x_vals = np.linspace(0, 10, 400)
    y_vals = c1 - x_vals

    # Limitar a la región donde x >= 0, y >= 0
    y_vals = np.maximum(0, y_vals)
    x_vals = np.maximum(0, x_vals)

    ax.fill_between(x_vals, 0, y_vals, alpha=0.3, color='lightgreen')
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Región Factible")

# Mostrar la región factible inicial
def mostrar_region_factible(c1=4):
    fig, ax = plt.subplots()
    restricciones_graficas(ax, c1)
    plt.show()

# Función para calcular y mostrar el valor de la función de costo en un punto dado
def mostrar_costo(x, y):
    valor = funcion_costo(x, y)
    messagebox.showinfo("Valor de la función de costo", f"El valor en ({x}, {y}) es: {valor}")

# Función para mostrar la gráfica 3D de la función f(x, y)
def mostrar_grafica_3d():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x_vals = np.linspace(-10, 10, 400)
    y_vals = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = funcion_costo(X, Y)

    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x, y)')
    plt.show()

# Ventana para calcular el valor de la función en un punto (x, y)
def ventana_calculo_costo():
    window = tk.Toplevel()
    window.title("Calcular Función de Costo en (x, y)")

    tk.Label(window, text="Valor de x:").pack()
    x_val = tk.Entry(window)
    x_val.pack()

    tk.Label(window, text="Valor de y:").pack()
    y_val = tk.Entry(window)
    y_val.pack()

    def calcular_valor():
        x = float(x_val.get())
        y = float(y_val.get())
        mostrar_costo(x, y)

    tk.Button(window, text="Calcular", command=calcular_valor).pack()

# Ventana para graficar la región factible ante un cambio en las restricciones
def ventana_graficar_region():
    window = tk.Toplevel()
    window.title("Graficar Región Factible")

    tk.Label(window, text="Ingrese nuevo valor para la restricción (x + y <=):").pack()
    restriccion_val = tk.Entry(window)
    restriccion_val.pack()

    def graficar_region():
        c1 = float(restriccion_val.get())
        mostrar_region_factible(c1)

    tk.Button(window, text="Graficar", command=graficar_region).pack()

# Ventana de optimización principal
def ventana_opcion1():
    window = tk.Toplevel()
    window.title("Optimización de Dos Variables")

    # Mostrar la función de costo y la gráfica 3D
    tk.Label(window, text="Función de costo: f(x, y) = x^2 + y^2").pack(pady=10)
    tk.Button(window, text="Mostrar gráfica 3D de f(x, y)", command=mostrar_grafica_3d).pack(pady=10)

    # Opciones para calcular el valor de la función de costo o graficar la región factible
    tk.Button(window, text="Calcular valor de la función de costo en un punto (x, y)", command=ventana_calculo_costo).pack(pady=10)
    tk.Button(window, text="Graficar la región factible ante un cambio de restricciones", command=ventana_graficar_region).pack(pady=10)

    # Mostrar la región factible inicial
    tk.Button(window, text="Mostrar región factible inicial", command=mostrar_region_factible).pack(pady=10)
