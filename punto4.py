import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy.optimize import minimize
import time

# Definir las funciones objetivo y sus Jacobianos
def funciones_disponibles():
    return {
        "x^2 + y^2": lambda x: x[0]**2 + x[1]**2,
        "Rosenbrock": lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2,
        "Beale": lambda x: (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2,
    }

# Función para los jacobianos
def jacobianos_disponibles():
    return {
        "x^2 + y^2": lambda x: np.array([2 * x[0], 2 * x[1]]),  # Gradiente de x^2 + y^2
        "Rosenbrock": lambda x: np.array([-400 * x[0] * (x[1] - x[0]**2) - 2 * (1 - x[0]), 200 * (x[1] - x[0]**2)]),
    }

# Lista de métodos de optimización
def metodos_disponibles():
    return ["Newton-CG", "Nelder-Mead", "BFGS"]

# Función para ejecutar la optimización y medir el tiempo
def ejecutar_optimizacion(metodo, funcion, jacobiano, x0, tolerancia, max_iter):
    inicio = time.perf_counter()

    # Si el método es Newton-CG, pasamos el jacobiano
    if metodo == "Newton-CG":
        resultado = minimize(funcion, x0, method=metodo, jac=jacobiano, tol=tolerancia, options={'maxiter': max_iter})
    else:
        resultado = minimize(funcion, x0, method=metodo, tol=tolerancia, options={'maxiter': max_iter})

    fin = time.perf_counter()
    tiempo_ejecucion = (fin - inicio) * 1e9  # Convertir a nanosegundos

    return resultado, tiempo_ejecucion

# Mostrar los resultados en la interfaz
def mostrar_resultados(tabla, resultados):
    for i, (parametros, tiempo) in enumerate(resultados):
        tabla.insert("", "end", values=(parametros["metodo"], parametros["funcion"], parametros["tolerancia"], parametros["max_iter"], round(tiempo, 2)))

# Función que ejecuta la optimización con varios parámetros y actualiza la tabla
def optimizar(tabla, metodo, funcion, x0, tolerancias, iteraciones):
    resultados = []
    funcion_objetivo = funciones_disponibles()[funcion]
    
    # Obtener el jacobiano solo si existe para la función
    jacobiano = jacobianos_disponibles().get(funcion, None)
    
    for tol in tolerancias:
        for max_iter in iteraciones:
            parametros = {"metodo": metodo, "funcion": funcion, "tolerancia": tol, "max_iter": max_iter}
            try:
                _, tiempo = ejecutar_optimizacion(metodo, funcion_objetivo, jacobiano, x0, tol, max_iter)
                resultados.append((parametros, tiempo))
            except Exception as e:
                messagebox.showerror("Error en la optimización", f"Error: {e}")

    mostrar_resultados(tabla, resultados)

# Interfaz principal para seleccionar el algoritmo y mostrar los resultados
def ventana_opcion4():
    window = tk.Toplevel()
    window.title("Algoritmos de Optimización Sin Restricciones")
    
    # Menú de selección para algoritmos y funciones objetivo
    tk.Label(window, text="Seleccione el algoritmo:").pack()
    metodo_var = tk.StringVar(window)
    metodo_var.set(metodos_disponibles()[0])
    tk.OptionMenu(window, metodo_var, *metodos_disponibles()).pack()

    tk.Label(window, text="Seleccione la función objetivo:").pack()
    funcion_var = tk.StringVar(window)
    funcion_var.set("x^2 + y^2")
    tk.OptionMenu(window, funcion_var, *funciones_disponibles().keys()).pack()

    # Entradas para el punto inicial
    tk.Label(window, text="Ingrese el punto inicial (x, y):").pack()
    x0_val = tk.Entry(window)
    x0_val.insert(0, "1,1")
    x0_val.pack()

    # Entradas para los parámetros de la optimización
    tk.Label(window, text="Tolerancias (separadas por comas):").pack()
    tolerancias_val = tk.Entry(window)
    tolerancias_val.insert(0, "1e-6,1e-5,1e-4")
    tolerancias_val.pack()

    tk.Label(window, text="Máximo de iteraciones (separados por comas):").pack()
    iteraciones_val = tk.Entry(window)
    iteraciones_val.insert(0, "100,200,500")
    iteraciones_val.pack()

    # Crear tabla para mostrar resultados
    columnas = ("Algoritmo", "Función", "Tolerancia", "Máximo Iteraciones", "Tiempo (ns)")
    tabla = ttk.Treeview(window, columns=columnas, show='headings')
    for col in columnas:
        tabla.heading(col, text=col)
    tabla.pack()

    # Función para ejecutar la optimización y llenar la tabla
    def ejecutar():
        x0 = list(map(float, x0_val.get().split(',')))
        tolerancias = list(map(float, tolerancias_val.get().split(',')))
        iteraciones = list(map(int, iteraciones_val.get().split(',')))
        optimizar(tabla, metodo_var.get(), funcion_var.get(), x0, tolerancias, iteraciones)

    # Botón para ejecutar la optimización
    tk.Button(window, text="Optimizar", command=ejecutar).pack()

# Fin del módulo optimizacion_sin_restricciones.py
