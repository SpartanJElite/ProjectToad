from socket import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import os
import pandas as pd

def animate(i):
    data = pd.read_csv(r'C:/Users/spong/Documents/Coding/Python/Motor2.csv')
    t = data['Time']
    x = data['EncoderAngle']
    y = data['Speed']
    plt.cla()
    plt.plot(t,x)

    plt.tight_layout()
    plt.title('Motor 2:Angular Position vs Time')
    plt.ylabel('Angular Position [deg]')
    plt.xlabel('Time [s]')


ani = FuncAnimation(plt.gcf(),animate,interval = 50)
plt.show()