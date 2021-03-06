from socket import *
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import ctypes
import os
import pandas as pd

def animate(i):
    data = pd.read_csv('Motor2.txt')
    t = data['Time']
    x = data['EncoderAngle']

    plt.cla()
    plt.plot(t,x)

    plt.tight_layout()

ani = FuncAnimation(plt.gcf(),animate,interval = 1000)
plt.show()