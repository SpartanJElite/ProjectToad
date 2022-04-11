from socket import *
from time import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import ctypes
import os
import pandas as pd
import numpy as np
import math
from scipy.integrate import odeint

global output1
global time1
output1 = []
time1 = []
global output2
global time2
output2 = []
time2 = []
global output3
output3 = []
time3 = []

global ySol
global dySolx
global dySoly
global dySolz

def millis():
        "return a timestamp in milliseconds (ms)"
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()

        #get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics)) 
        #get the actual freq. of the internal ~2MHz QPC clock 
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq)) 
        
        t_ms = tics.value*1e3/freq.value
        return t_ms

def Motor1():
    adress = ('192.168.1.117',2390)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    counter = 1
    output = []
    data = 80
    increase = 1

    pathName = 'C:/Users/spong/Documents/Coding/Python'
    fileName = 'Motor1.csv'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,"w")
    newFile.write("Time,EncoderAngle,Speed")
    newFile.write("\n")
    p = 1
    i = 0

    while(counter == 1):
        if(i >= len(dySolx)):
            i = 0
        data = dySolx[i]
        i = i+1
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            temp = float(temp)
            output1.append(temp)
            time1.append(millis())
            vel1 = velocityFunc(output1,time1)
            print("Motor1 ON")
            if(p == -1):
                newFile.write(str(time1[-1]))
                newFile.write(",")
                newFile.write(str(output1[-1]))
                newFile.write(",")
                newFile.write(str(vel1[-1]))
                newFile.write("\n")
            if(p != -1):
                p = p + 1
                if(p == 4):
                    p = -1
        except:
            print("Error")
        
    return output

def Motor2():
    adress = ('192.168.1.128',2390)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    counter = 1
    output = []
    data = 90
    increase = 1

    pathName = 'C:/Users/spong/Documents/Coding/Python'
    fileName = 'Motor2.csv'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,"w")
    newFile.write("Time,EncoderAngle,Speed")
    newFile.write("\n")
    p = 1
    i = 0
    while(counter == 1):
        if(i >= len(dySoly)):
            i = 0
        data = dySoly[i]
        i = i+1
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            temp = float(temp)
            output2.append(temp)
            time2.append(millis())
            vel2 = velocityFunc(output2,time2)
            print("Motor2 ON")
            if(p == -1):
                newFile.write(str(time2[-1]))
                newFile.write(",")
                newFile.write(str(output2[-1]))
                newFile.write(",")
                newFile.write(str(vel2[-1]))
                newFile.write("\n")
            if(p != -1):
                p = p + 1
                if(p == 4):
                    p = -1
        except:
            print("Error")
            #counter = 0
    return output

def Motor3():
    adress = ('172.20.10.4',2390)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    counter = 1
    output = []
    data = 0

    pathName = 'C:/Users/spong/Documents/Coding/Python'
    fileName = 'Motor3.csv'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,"w")
    newFile.write("Time,EncoderAngle,Speed")
    newFile.write("\n")
    p = 1
    #i = 0
    i = 1
    while(counter == 1):
        # if(i >= (len(dySolz))):
        #     i = 0
        #data = dySolz[i]
        if(i >= (len(ySol[:,2])-1)):
            i = 1
        data = ySol[i,2]
        i = i+1
        print(str(data).encode('utf-8'))
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            temp = float(temp)
            output3.append(temp)
            time3.append(millis())
            vel3 = velocityFunc(output3,time3)
            print("Motor3 ON")
            if(p == -1):
                newFile.write(str(time3[-1]))
                newFile.write(",")
                newFile.write(str(output3[-1]))
                newFile.write(",")
                newFile.write(str(vel3[-1]))
                newFile.write("\n")
            if(p != -1):
                p = p + 1
                if(p == 4):
                    p = -1
        except:
            counter = 0
    return output
def parseFunc(output):
    t = []
    val = []
    n = len(output)
    if((n%2)==1):
        del output[-1]
    for i in range(0,len(output)):
        if((i%2)==1):
            val.append(output[i])
        if((i%2)==0):
            t.append(output[i])
    return t,val
def velocityFunc(val,t):
    vel = []
    for i in range(1,len(t)-1):
        vtemp = (val[i+1]-val[i-1])/(t[i+1]-t[i-1])
        vel.append(vtemp)
    return vel
def angle2quat(r1,r2,r3):
    angles = np.array([r1,r2,r3])
    cang = np.array([math.cos(angles[0]/2),math.cos(angles[1]/2),math.cos(angles[2]/2)])
    sang = np.array([math.sin(angles[0]/2),math.sin(angles[1]/2),math.sin(angles[2]/2)])
    q = [ cang[0]*cang[1]*cang[2] + sang[0]*sang[1]*sang[2],
            cang[0]*cang[1]*sang[2] - sang[0]*sang[1]*cang[2],
            cang[0]*sang[1]*cang[2] + sang[0]*cang[1]*sang[2],
            sang[0]*cang[1]*cang[2] - cang[0]*sang[1]*sang[2]]
    return q

def odes(x,t,w):
    coeff = np.array([[0, -w[0], -w[1], -w[2]],
                    [w[0], 0, w[2], -w[1]], 
                    [w[1], -w[2], 0, w[0]], 
                    [w[2], w[1], -w[0], 0]])
    dY = (1.0/2.0)*np.matmul(coeff,x)   
    return dY

def quat2angles(x, y, z, w):
    roll_x=math.atan2(2*(x*y+z*w),1-2*(y*y+z*z))
    pitch_y=math.asin(2*(x*z-w*y))
    yaw_z=math.atan2(2*(x*w+y*z),1-2*(z*z+w*w))
    return yaw_z,pitch_y,roll_x



def array_quat2eul(ySol):
    toRad=2*np.pi/360
    toDeg=1/toRad
    euler = np.zeros((len(ySol),3))
    for i in range(0,len(ySol)):
        [yaw,pitch,roll] = quat2angles(ySol[i,0],ySol[i,1],ySol[i,2],ySol[i,3])
        euler[i,:] = np.array([yaw,pitch,roll])*toDeg
    return euler

def velocityFunc2(val,t):
    vel = []
    for i in range(1,len(t)-1):
        vtemp = (val[i+1]-val[i-1])/(t[i+1]-t[i-1])
        if(vtemp > 1000 or vtemp < -1000):
            vtemp = vel[-1]
        vel.append(vtemp)
    return vel

def map(val,inMin,inMax,outMin,outMax):
    return (val-inMin)*(outMax-outMin)/(inMax - inMin)+outMin

def scalemap(x,y,z):
    for i in range(0,len(x)):
        x[i] = x[i] + 90
        y[i] = y[i] + 90
        z[i] = z[i] + 90
    xMax = max(x)
    yMax = max(y)
    zMax = max(z)
    maxVec = [xMax,yMax,zMax]
    valMax = max(maxVec)
    xMin = min(x)
    yMin = min(y)
    zMin = min(z)
    minVec = [xMin,yMin,zMin]
    valMin = min(minVec)
    dx = map(x,valMin,valMax,0,180)
    dy = map(y,valMin,valMax,0,180)
    dz = map(z,valMin,valMax,0,180)
    return dx,dy,dz

toRad=2*np.pi/360
toDeg=1/toRad

w = [0,1,1]
yaw = 0 *toRad
pitch = 0 *toRad
roll = 0 *toRad
quat = angle2quat(yaw,pitch,roll)
t = np.linspace(0,60,6001)
ySol = odeint(odes,quat,t,args=(w,))
ySol = array_quat2eul(ySol)



dySolx = velocityFunc2(ySol[:,0],t)
dySoly = velocityFunc2(ySol[:,1],t)
dySolz = velocityFunc2(ySol[:,2],t)
[dySolx,dySoly,dySolz]=scalemap(dySolx,dySoly,dySolz)

plt.subplot(6,1,1)
plt.plot(t,ySol[:,0])

plt.subplot(6,1,2)
plt.plot(t,ySol[:,1])

plt.subplot(6,1,3)
plt.plot(t,ySol[:,2])

plt.subplot(6,1,4)
plt.plot(t[1:len(t)-1],dySolx)

plt.subplot(6,1,5)
plt.plot(t[1:len(t)-1],dySoly)

plt.subplot(6,1,6)
plt.plot(t[1:len(t)-1],dySolz)

plt.show()

#motor1Thread = Thread(target=Motor1)
#motor2Thread = Thread(target=Motor2)
#motor3Thread = Thread(target=Motor3)


#motor1Thread.daemon=True
#motor2Thread.daemon=True
#motor3Thread.daemon=True



#motor1Thread.start()
#motor2Thread.start()
#motor3Thread.start()


#motor1Thread.join()
#motor2Thread.join()
#motor3Thread.join()