# %%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 15:08:30 2019
@author: Rodolfo E. Escobar U.
"""
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")
# %%


def B0f():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(4 * x)
    ax.clear()
    ax.plot(x, y), ax.grid(True)
    ax.set_xlabel("$x$"), ax.set_ylabel("$y(x)$")
    ax.set_title("$y(x)=sin(4x)$")
    line.draw()


def B1f():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(4 * x)
    ax.clear()
    ax.plot(x, y), ax.grid(True)
    ax.set_xlabel("$x$"), ax.set_ylabel("$y(x)$")
    ax.set_title("$y(x)=cos(4x)$")
    line.draw()


def B2f():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.exp(-0.5 * x) * np.sin(4 * x)
    ax.clear()
    ax.plot(x, y), ax.grid(True)
    ax.set_xlabel("$x$"), ax.set_ylabel("$y(x)$")
    ax.set_title("$y(x)=e^{-0.5x}sin(4x)$")
    line.draw()


def B3f():
    x = np.linspace(0, 10, 100)
    y = np.exp(x)
    ax.clear()
    ax.plot(x, y), ax.grid(True)
    ax.set_xlabel("$x$"), ax.set_ylabel("y(x)")
    ax.set_title("$y(x) = e^{x}$")
    line.draw()


def B4f():
    def gaussian(x, mu, sig):
        return (
            1.0
            / (np.sqrt(2.0 * np.pi) * sig)
            * np.exp(-np.power((x - mu) / sig, 2.0) / 2)
        )

    x = np.linspace(0, 10, 100)
    y = gaussian(x, 5, 1.3)
    ax.clear()
    ax.plot(x, y), ax.grid(True)
    ax.set_xlabel("$x$"), ax.set_ylabel("y(x)")
    ax.set_title("$y(x) = Gaussian(x,5,1.3)$")
    line.draw()


# %%


# --- Raiz ---
root = tk.Tk()
root.geometry("940x450")
root.title("Tkinter + Matplotlib")
# ------------
# %%

# -- Frames ---
left_frame = tk.Frame(root)
left_frame.place(relx=0.03, rely=0.05, relwidth=0.25, relheight=0.9)

right_frame = tk.Frame(root, bg="#C0C0C0", bd=1.5)
right_frame.place(relx=0.3, rely=0.05, relwidth=0.65, relheight=0.9)
# ---------------
# %%

# --- Botones ---
RH = 0.19

B0 = tk.Button(left_frame, text="SIN(4x)", command=B0f)
B0.place(relheight=RH, relwidth=1)

B1 = tk.Button(left_frame, text="COS(4x)", command=B1f)
B1.place(rely=(0.1 + RH * 0.54), relheight=RH, relwidth=1)

B2 = tk.Button(left_frame, text="EXP(-0.5x)SIN(x)", command=B2f)
B2.place(rely=2 * (0.1 + RH * 0.54), relheight=RH, relwidth=1)

B3 = tk.Button(left_frame, text="EXP(x)", command=B3f)
B3.place(rely=3 * (0.1 + RH * 0.54), relheight=RH, relwidth=1)

B4 = tk.Button(left_frame, text="Gaussian(x)", command=B4f)
B4.place(rely=4 * (0.1 + RH * 0.54), relheight=RH, relwidth=1)
# ------------
# %%

# --- Agregar figura ---
figure = plt.Figure(figsize=(5, 6), dpi=100)
ax = figure.add_subplot(111)
ax.grid(True), ax.set_xlabel("$x$"), ax.set_ylabel("$y(x)$")
line = FigureCanvasTkAgg(figure, right_frame)
line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
# ----------------------

root.mainloop()
