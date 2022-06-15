import numpy as np
import serial
import time
import matplotlib.pyplot as plt
import re

# Serial arduino
serialArduino = serial.Serial("COM4", 9600, timeout=1.0)

# decimos de forma explícita que sea interactivo
plt.ion()
i = 0  # contador

# los datos que vamos a dibujar y a actualizar
x = []
y_ax, y_ay, y_az = [], [], []
fig, ax = plt.subplots()

# el bucle infinito que irá dibujando
while True:
    # y.append(np.random.randn(1)) # añadimos un valor aleatorio a la lista 'y'
    # leemos la linea del serial en arduino
    cad = serialArduino.readline().decode("ascii")

    # Los primeros datos son basura, inicio en 0
    if i == 0:
        cad1 = 0
        cad2 = 0
        cad3 = 9.81
    else:
        # recupero los valores flotantes de la lectura de linea
        cad1, cad2, cad3 = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", cad)

    # convertimos a un dato flotante
    x.append(float(i))
    y_ax.append(float(cad1))
    y_ay.append(float(cad2))
    y_az.append(float(cad3))

    # Esta condición es para graficar constantemente los últimos
    # 10 datos de la lista 'x' y 'y' ya que quiero que en el gráfico se
    # vea la evolución de los últimos datos, se actualiza sola
    if len(y_ax) <= 10:
        plt.plot(x, y_ax)
        plt.plot(x, y_ay)
        plt.plot(x, y_az)
    else:
        # actualizo datos de X y Y
        plt.plot(x[-10:], y_ax[-10:])
        plt.plot(x[-10:], y_ay[-10:])
        plt.plot(x[-10:], y_az[-10:])

    # Actualizo contador para eje x
    i += 1

    # Datos de gráfica
    ax.set_ylim([-10, 10])
    plt.title("Sensor")
    plt.xlabel("X-Axis")
    plt.ylabel("Aceleración (N)")
    plt.pause(0.05)  # esto pausará el gráfico
    plt.cla()  # esto limpia la información del axis (el área blanca)

# arduinoSerialData.close()
cv2.waitKey(0)
cv2.destroyAllWindows()
