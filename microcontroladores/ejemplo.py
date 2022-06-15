# %%
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import sin
# %%

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize communication with TMP102


def datos():
    num = 0
    while True:
        yield sin(num)
        num += 0.3


siguiente_dato = datos()

# %%
# This function is called periodically from FuncAnimation


def animate(i, xs, ys):
    # Read temperature (Celsius) from TMP102
    temp_c = next(siguiente_dato)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')


# %%
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
plt.show()
