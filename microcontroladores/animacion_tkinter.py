# %%
"""Librerías para manejar de interfaz gráfica y animaciones
de gráficas."""
from tkinter import Tk, Frame, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# %%
# Create figure for plotting
fig, ax = plt.subplots()
XS, YS = [], []

# Crea la dirección donde se guardarán los datos
nombre_carpeta = "datos"
nombre_archivo = (
    f"{nombre_carpeta}\\{dt.datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.csv"
)
if not os.path.exists(nombre_carpeta):
    os.mkdir(nombre_carpeta)
    print(f"Creada la carpeta {nombre_carpeta}")

# %%
with open(nombre_archivo, "a", encoding="utf-8") as datos:
    datos.write("Tiempo,Temperatura\n")
# Initialize communication with TMP102


# %%
def animate(i, xs, ys):
    # Read temperature (Celsius) from TMP102
    temp_c = np.random.uniform()
    # Add x and y to lists
    marca_de_tiempo = dt.datetime.now()
    xs.append(marca_de_tiempo.strftime("%H:%M:%S.%f")[:-4])
    ys.append(temp_c)

    with open(nombre_archivo, "a", encoding="utf-8") as datos:
        datos.write(f"{marca_de_tiempo.strftime('%d-%m-%Y %H:%M:%S.%f')},{temp_c}\n")
        # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.30)
    plt.title("Temperatura Vs Tiempo")
    plt.ylabel("Temperatura (°C)")


ANI = animation.FuncAnimation(fig, animate, fargs=(XS, YS), interval=10)


def pausar():
    """Pausa la animación de la gráfica."""
    global ANI
    ANI.event_source.stop()


def reanudar():
    global ANI
    """Reanuda la animación de la gráfica."""
    ANI.event_source.start()


# %%
ventana = Tk()
ventana.geometry("642x535")
ventana.wm_title("Grafica Matplotlib Animacion")
ventana.minsize(width=642, height=535)

frame = Frame(ventana, bg="white", bd=3)
frame.pack(expand=1, fill="both")

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(padx=5, pady=5, expand=1, fill="both")
# %%
Button(frame, text="Pausar", width=15, bg="salmon", fg="white", command=pausar).pack(
    pady=5, side="left", expand=1
)

Button(frame, text="Reanudar", width=15, bg="green", fg="white", command=reanudar).pack(
    pady=5, side="left", expand=1
)

ventana.mainloop()
