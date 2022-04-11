from socket import *
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import ctypes
import os
import pandas as pd


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
    while(counter == 1):
        # if((data > 130) or (data < 50)):
        #     increase = increase * -1
        data = 90
        #print(data)
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            temp = float(temp)
            output1.append(temp)
            print("Motor 1:",millis())
            time1.append(millis())
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
    while(counter == 1):
        if((data > 130) or (data < 50)):
            increase = increase * -1
        data = data + increase
        data = 85
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
    while(counter == 1):
        data = data + 1
        if(data >= 360):
            data = 0
        print(str(data).encode('utf-8'))
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            temp = float(temp)
            output3.append(temp)
            print("Motor 3:",millis())
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
def ploting():
    ani = FuncAnimation(plt.gcf(),animate,interval = 1000)
    plt.show()

def animate(i):
    data = pd.read_csv('Motor2.txt')
    t = data['Time']
    x = data['EncoderAngle']

    plt.cla()
    plt.plot(t,x)

    plt.tight_layout()

threads1 = []
#motor1Thread = Thread(target=Motor1)
motor2Thread = Thread(target=Motor2)
#motor3Thread = Thread(target=Motor3)


#motor1Thread.daemon=True
motor2Thread.daemon=True
#motor3Thread.daemon=True



#motor1Thread.start()
motor2Thread.start()
#motor3Thread.start()


#motor1Thread.join()
motor2Thread.join()
#motor3Thread.join()


#[angle,t] = parseFunc(output1)

# angle = output1
# t = time1
# vel = velocityFunc(angle,t)

# plot1 = plt. figure(1)
# plt.plot(t,angle)
# plt.title('Motor 1:Angular Position vs Time')
# plt.ylabel('Angular Position [deg]')
# plt.xlabel('Time [s]')

# plot2 = plt.figure(2)
# plt.plot(t[1:len(t)-1],vel)
# plt.title('Motor 1:Angular Velocity vs Time')
# plt.ylabel('Angular Velocity [deg/s]')
# plt.xlabel('Time [s]')
# plt.show()

angle2 = output2
t2 = time2
vel2 = velocityFunc(angle2,t2)

plot3 = plt. figure(3)
plt.plot(t2,angle2)
plt.title('Motor 2:Angular Position vs Time')
plt.ylabel('Angular Position [deg]')
plt.xlabel('Time [s]')

plot4 = plt.figure(4)
plt.plot(t2[1:len(t2)-1],vel2)
plt.title('Motor 2:Angular Velocity vs Time')
plt.ylabel('Angular Velocity [deg/s]')
plt.xlabel('Time [s]')
plt.show()

    
