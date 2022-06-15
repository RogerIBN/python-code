# %%
'''Librerías para manejor de interfaz gráfica y animaciones
de gráficas.'''
from tkinter import Tk, Frame, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# %%
fig, ax = plt.subplots(facecolor='#05FFBF')
plt.title("Grafica en Tkinter con ...", color='black', size=16, family="Arial")

i = 0
x = np.arange(0, 4*np.pi, 0.01)
line, = ax.plot(x, np.sin(x), color='m', marker='o', linestyle='dotted',
                linewidth=5, markersize=1, markeredgecolor='m')  # dotter, dashdot, dashed

# %%


def animate(i):
    line.set_ydata(np.sin(x + i/40))  # actualizar dato y
    # print(line)
    return line,


def iniciar():
    global ANI
    ANI = animation.FuncAnimation(
        fig, animate, interval=20, blit=True, save_count=10)
    '''Inicia la animación de la gráfica.'''
    canvas.draw()


def pausar():
    '''Pausa la animación de la gráfica.'''
    ANI.event_source.stop()


def reanudar():
    '''Reanuda la animación de la gráfica.'''
    ANI.event_source.start()


# %%
ventana = Tk()
ventana.geometry('642x535')
ventana.wm_title('Grafica Matplotlib Animacion')
ventana.minsize(width=642, height=535)

frame = Frame(ventana, bg='white', bd=3)
frame.pack(expand=1, fill='both')

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(padx=5, pady=5, expand=1, fill='both')
# %%
Button(frame, text='Grafica Datos', width=15, bg='purple4', fg='white',
       command=iniciar).pack(pady=5, side='left', expand=1)

Button(frame, text='Pausar', width=15, bg='salmon', fg='white',
       command=pausar).pack(pady=5, side='left', expand=1)

Button(frame, text='Reanudar', width=15, bg='green', fg='white',
       command=reanudar).pack(pady=5, side='left', expand=1)

ventana.mainloop()
