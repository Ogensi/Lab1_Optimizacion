import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Función para seleccionar la función
def seleccionar_funcion(opcion):
    x = sp.symbols('x')

    if opcion == "1. f(x) = sin(x)":
        return sp.sin(x), 'sin(x)'
    elif opcion =="2. f(x) = cos(x)":
        return sp.cos(x), 'cos(x)'
    elif opcion == "3. f(x) = exp(x)":
        return sp.exp(x), 'exp(x)'
    elif opcion ==  "4. f(x) = ln(1+x)":
        return sp.log(1 + x), 'ln(1+x)'
    elif opcion ==  "5. f(x) = 1/(1-x)":
        return 1 / (1 - x), '1/(1-x)'
    else:
        messagebox.showerror("Error", "Opción no válida")
        return None, None

# Función para calcular la expansión de Taylor
def expansion_taylor(funcion, punto, terminos):
    x = sp.symbols('x')
    taylor = 0
    n = 0
    while not n > terminos:
        derivada = sp.diff(funcion, x, n)
        derivada_x0 = derivada.subs(x, punto)
        divisor = sp.factorial(n)
        termino_taylor = (derivada_x0/divisor) * (x-punto)**n
        taylor += termino_taylor
        n += 1
    return taylor

# Función para graficar la función original y la serie de Taylor
def graficar(funcion, taylor_aprox, punto, rango, terminos, nombre_funcion, expresion_taylor_latex):
    x = np.linspace(rango[0], rango[1], 400)

    fun_lambd = sp.lambdify(sp.symbols('x'), funcion, "numpy")
    taylor_lambd = sp.lambdify(sp.symbols('x'), taylor_aprox, "numpy")

    y_fun = fun_lambd(x)
    y_taylor = taylor_lambd(x)

    plt.figure(figsize=(8, 6))

    plt.plot(x, y_fun, label="Función original", color="blue")
    plt.plot(x, y_taylor, label=f"Serie de Taylor ({terminos} términos)", linestyle="dashed", color="red")
    plt.scatter(punto, fun_lambd(punto), color="black", marker="o", label=f"Expansión en x={punto}")
    plt.text(0.05, 0.85, f"Polinomio de Taylor: ${expresion_taylor_latex}$", fontsize=10, transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))    
    plt.title(f"Aproximación de Taylor para {nombre_funcion}")
    plt.legend()
    plt.grid(True)
    plt.ylim(-5, 5)
    plt.show()

# Función para manejar la interfaz gráfica de Tkinter
def calcular_taylor():
    # Obtener los valores del menú y entradas de usuario
    try:
        #opcion = int(funcion_var.get())  # Aseguramos que la opción sea un número
        terminos = int(terminos_entry.get())
        punto = float(punto_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
        return

    # Seleccionar la función
    funcion, nombre_funcion = seleccionar_funcion(funcion_var.get())
    if funcion is None:
        return

    # Calcular la serie de Taylor
    taylor_aprox = expansion_taylor(funcion, punto, terminos)

    expresion_taylor_latex = sp.latex(taylor_aprox)

    # Graficar la función y la aproximación de Taylor
    rango = [-8, 8]
    graficar(funcion, taylor_aprox, punto, rango, terminos, nombre_funcion, expresion_taylor_latex)

# Función principal que crea la ventana de Tkinter
def ventana_opcion3():
    window = tk.Toplevel()
    window.title("Expansión en Series de Taylor")

    # Menú desplegable para seleccionar la función
    tk.Label(window, text="Seleccione la función:").pack()
    global funcion_var
    funcion_var = tk.StringVar(value="1")
    funciones_menu = tk.OptionMenu(window, funcion_var, "1. f(x) = sin(x)", "2. f(x) = cos(x)", "3. f(x) = exp(x)", "4. f(x) = ln(1+x)", "5. f(x) = 1/(1-x)")
    funciones_menu.pack()

    # Entrada para la cantidad de términos
    tk.Label(window, text="Cantidad de términos de la serie de Taylor:").pack()
    global terminos_entry
    terminos_entry = tk.Entry(window)
    terminos_entry.pack()

    # Entrada para el punto de expansión
    tk.Label(window, text="Punto de expansión (a):").pack()
    global punto_entry
    punto_entry = tk.Entry(window)
    punto_entry.pack()

    # Botón para calcular la serie de Taylor y graficar
    tk.Button(window, text="Calcular y Graficar", command=calcular_taylor).pack()

# Prueba del código sin necesidad del menú principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Expansión en Series de Taylor")
    ventana_opcion3()
    root.mainloop()
