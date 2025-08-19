import tkinter as tk
import algorithms
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter

lista = []
error_label = None

tiempos_lineal = {100: [], 1000: [], 10000: [], 100000: []}
tiempos_binaria = {100: [], 1000: [], 10000: [], 100000: []}

def actualizar_graficas():
    tamaños = [100, 1000, 10000, 100000]

    prom_lineal_s  = [ (sum(tiempos_lineal[t])/len(tiempos_lineal[t])) if tiempos_lineal[t] else 0 for t in tamaños ]
    prom_binaria_s = [ (sum(tiempos_binaria[t])/len(tiempos_binaria[t])) if tiempos_binaria[t] else 0 for t in tamaños ]

    prom_lineal_us  = [v * 1e6 for v in prom_lineal_s]
    prom_binaria_us = [v * 1e6 for v in prom_binaria_s]

    fig1 = Figure(figsize=(4,3), dpi=100)
    ax1 = fig1.add_subplot(111)
    bars1 = ax1.bar([str(t) for t in tamaños], prom_lineal_us)
    ax1.set_title("Búsqueda Lineal")
    ax1.set_ylabel("Promedio microsegundos (µs)")
    ax1.set_ylim(bottom=0) 
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.0f')) 

    try:
        ax1.bar_label(bars1, fmt='%.0f') 
    except Exception:
        pass 
    
    for widget in frame_grafica_lineal.winfo_children():
        widget.destroy()
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_grafica_lineal)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    fig2 = Figure(figsize=(4,3), dpi=100)
    ax2 = fig2.add_subplot(111)
    bars2 = ax2.bar([str(t) for t in tamaños], prom_binaria_us)    
    ax2.set_title("Búsqueda Binaria")
    ax2.set_ylabel("Promedio microsegundos (µs)")
    ax2.set_ylim(bottom=0)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    try:
        ax2.bar_label(bars2, fmt='%.0f')
    except Exception:
        pass
    
    for widget in frame_grafica_binaria.winfo_children():
        widget.destroy()
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_grafica_binaria)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def generar_lista_gui():
    global lista, error_label
    try:
        size = int(entry_size.get().strip())
        lista = algorithms.generar_lista(size)
        print("Lista generada: ", lista)
        if error_label is not None:
            error_label.destroy()
            error_label = None
    except ValueError:
        if error_label is None:
            error_label = tk.Label(root, text="⚠ Ingresa un número válido", fg="red")
            error_label.pack(after=btn)


def busqueda_lineal_gui():
    try:
        if not lista:
            resultado_lineal.config(text="No se ha creado la lista", fg="red")
            return
                
        objetivo = int(entry_objetivo.get().strip())
        inicio = time.perf_counter()
        pos = algorithms.busqueda_lineal(lista, objetivo)
        fin = time.perf_counter()
        tiempo_ejecucion = fin - inicio
        n = len(lista)

        if n in tiempos_lineal:
            tiempos_lineal[n].append(tiempo_ejecucion)
            actualizar_graficas()

        if pos != -1:
            resultado_lineal.config(
                text=f"Tamaño de la lista: {n}\nNúmero {objetivo} encontrado\nPosición: {pos}\nTiempo: {tiempo_ejecucion:.6f} segundos",
                fg="blue"
            )
        else:
            resultado_lineal.config(
                text=f"Tamaño de la lista: {n}\nNúmero {objetivo} no encontrado\nTiempo: {tiempo_ejecucion:.6f} segundos",
                fg="red"
            )
    except ValueError:
        resultado_lineal.config(text="⚠ Ingresa un número válido", fg="red")


def busqueda_binaria_gui():
    try:
        if not lista:
            resultado_binaria.config(text="No se ha creado la lista", fg="red")
            return
        objetivo = int(entry_objetivo.get().strip())
        lista_ordenada = sorted(lista)
        
        inicio = time.perf_counter()        
        pos = algorithms.busqueda_binaria(lista_ordenada, objetivo)        
        fin = time.perf_counter()
        tiempo_ejecucion = fin - inicio
        n = len(lista)

        if n in tiempos_binaria:
            tiempos_binaria[n].append(tiempo_ejecucion)
            actualizar_graficas()

        if pos != -1:
            resultado_binaria.config(
                text=f"Tamaño de la lista: {n}\nNúmero {objetivo} encontrado\nPosición: {pos}\nTiempo: {tiempo_ejecucion:.6f} segundos",
                fg="blue"
            )
        else:
            resultado_binaria.config(
                text=f"Tamaño de la lista: {n}\nNúmero {objetivo} no encontrado\nTiempo: {tiempo_ejecucion:.6f} segundos",
                fg="red"
            )
            
    except ValueError:
        resultado_binaria.config(text="⚠ Ingresa un número válido", fg="red")


def iniciar_aplicacion():
    global root, entry_size, entry_objetivo, resultado_lineal, resultado_binaria, btn
    global frame_grafica_lineal, frame_grafica_binaria

    root = tk.Tk()
    root.title("Comparación de Búsquedas")
    root.geometry("1100x800")

    tk.Label(root, text="Tamaño de lista:").pack(pady=5)
    entry_size = tk.Entry(root)
    entry_size.pack(pady=5)

    btn = tk.Button(root, text="Generar lista", command=generar_lista_gui)
    btn.pack(pady=10)

    tk.Label(root, text="Número a buscar:").pack(pady=5)
    entry_objetivo = tk.Entry(root)
    entry_objetivo.pack(pady=5)

    contenedor_frames = tk.Frame(root)
    contenedor_frames.pack(pady=5)

    frame_resultado_lineal = tk.Frame(contenedor_frames, width=300, height=120, relief="groove", borderwidth=2)
    frame_resultado_lineal.pack_propagate(False)
    frame_resultado_lineal.pack(side="left", padx=120)

    frame_resultado_binaria = tk.Frame(contenedor_frames, width=300, height=120, relief="groove", borderwidth=2)
    frame_resultado_binaria.pack_propagate(False)
    frame_resultado_binaria.pack(side="right", padx=120)

    boton_lineal = tk.Button(frame_resultado_lineal, text="Búsqueda Lineal", command=busqueda_lineal_gui)
    boton_lineal.pack(pady=5)

    boton_binaria = tk.Button(frame_resultado_binaria, text="Búsqueda Binaria", command=busqueda_binaria_gui)
    boton_binaria.pack(pady=5)

    resultado_lineal = tk.Label(frame_resultado_lineal, text="", wraplength=280, justify="left")
    resultado_lineal.pack(pady=10)

    resultado_binaria = tk.Label(frame_resultado_binaria, text="", wraplength=280, justify="left")
    resultado_binaria.pack(pady=10)

    frame_graficas = tk.Frame(root)
    frame_graficas.pack(fill="both", expand=True, pady=20)

    frame_grafica_lineal = tk.Frame(frame_graficas, width=500, height=300, relief="ridge", borderwidth=2)
    frame_grafica_lineal.pack(side="left", padx=10, fill="both", expand=True)

    frame_grafica_binaria = tk.Frame(frame_graficas, width=500, height=300, relief="ridge", borderwidth=2)
    frame_grafica_binaria.pack(side="right", padx=10, fill="both", expand=True)

    root.mainloop()

