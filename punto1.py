import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

   
def funcion_costo(x, y):
    return 3*(x**2) + 2*(y**2) + 80 #Sacada de https://totumat.com/2020/04/13/optimizacion-con-restricciones/

# Gráfica 3D de la función de costo con restricción x + y = 30
def graficar_region_factible(c=30):
    x_vals = np.linspace(0, c, 100)
    y_vals = c - x_vals  # Restricción: x + y = c
    
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = funcion_costo(X, Y)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
    ax.set_title(f"Función de costo: $3x^2 + 2y^2 + 80$, Restricción: $x + y = {c}$")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x, y)')
    
    plt.show()

# Mostrar el valor de la función de costo en un punto (x, y)
def calcular_valor_funcion(x, y):
    valor = funcion_costo(x, y)
    messagebox.showinfo("Valor de la Función de Costo", f"El valor de f({x}, {y}) es: {valor}")

# Opción para ver cómo cambia la región factible ante cambios en la restricción
def mostrar_region_factible(c):
    graficar_region_factible(c)

def ventana_opcion1():
    window = tk.Toplevel()
    window.title("Optimización de Dos Variables")

    # Mostrar la gráfica inicial con la restricción x + y = 30
    tk.Label(window, text="Gráfica de la región factible inicial (x + y = 30):").pack()
    tk.Button(window, text="Mostrar Gráfica", command=lambda: graficar_region_factible(30)).pack(pady=10)

    # Opción a: Ingresar el punto (x, y) y calcular el valor de la función de costo
    tk.Label(window, text="Calcular el valor de la función de costo en un punto (x, y):").pack(pady=5)
    
    tk.Label(window, text="Valor de x:").pack()
    x_val = tk.Entry(window)
    x_val.pack()

    tk.Label(window, text="Valor de y:").pack()
    y_val = tk.Entry(window)
    y_val.pack()

    def calcular_valor():
        x = float(x_val.get())
        y = float(y_val.get())
        calcular_valor_funcion(x, y)

    tk.Button(window, text="Calcular Valor de la Función", command=calcular_valor).pack(pady=10)

    # Opción b: Modificar la restricción y mostrar la nueva región factible
    tk.Label(window, text="Modificar la restricción (x + y = c) y mostrar la región factible:").pack(pady=5)

    tk.Label(window, text="Nuevo valor de c:").pack()
    c_val = tk.Entry(window)
    c_val.pack()

    def mostrar_nueva_region():
        c = float(c_val.get())
        mostrar_region_factible(c)

    tk.Button(window, text="Mostrar Nueva Región Factible", command=mostrar_nueva_region).pack(pady=10)
