from socket import *
import time
import matplotlib.pyplot as plt
from threading import Thread
import numpy as np
from math import *
from scipy.integrate import odeint


global output1
output1 = []
global output2
output2 = []
global output3
output3 = []

def Motor1():
    adress = ('172.20.10.4',2390)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    counter = 1
    output = []
    data = 0
    increase = 1
    while(counter == 1):
        if((data > 120) or (data < 0)):
            increase = increase * -1
        data = data + increase
        #print(data)
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            print(1)
            temp = float(temp)
            output1.append(temp)
            time.sleep(0.000)
        except:
            counter = 0
    return output

def Motor2():
    adress = ('172.20.10.3',2390)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    counter = 1
    output = []
    data = 0
    while(counter == 1):
        data = data + 1
        if(data >= 360):
            data = 0
        client_socket.sendto(str(data).encode('utf-8'),adress)
        try:
            [rec_data,addr] = client_socket.recvfrom(2048)
            temp = rec_data.decode('utf-8')
            print(2)
            temp = float(temp)
            output2.append(temp)
            time.sleep(0.000)
        except:
            counter = 0
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
            print(temp)
            temp = float(temp)
            output3.append(temp)
            time.sleep(0.000)
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
    cang = np.array([cos(angles[0]/2),cos(angles[1]/2),cos(angles[2]/2)])
    sang = np.array([sin(angles[0]/2),sin(angles[1]/2),sin(angles[2]/2)])
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
    roll_x=atan2(2*(x*y+z*w),1-2*(y*y+z*z))
    pitch_y=asin(2*(x*z-w*y))
    yaw_z=atan2(2*(x*w+y*z),1-2*(z*z+w*w))
    return yaw_z,pitch_y,roll_x



def array_quat2eul(ySol):
    toRad=2*np.pi/360
    toDeg=1/toRad
    euler = np.zeros((len(ySol),3))
    for i in range(0,len(ySol)):
        [yaw,pitch,roll] = quat2angles(ySol[i,0],ySol[i,1],ySol[i,2],ySol[i,3])
        euler[i,:] = np.array([yaw,pitch,roll])*toDeg
    return euler

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

threads1 = []

motor1Thread = Thread(target=Motor1)
motor2Thread = Thread(target=Motor2)
#motor3Thread = Thread(target=Motor3)
motor1Thread.daemon=True
motor2Thread.daemon=True
#motor3Thread.daemon=True


motor1Thread.start()
motor2Thread.start()
#motor3Thread.start()

motor1Thread.join()
motor2Thread.join()
#motor3Thread.join()

[angle,t] = parseFunc(output1)
vel = velocityFunc(angle,t)

plot1 = plt. figure(1)
plt.plot(t,angle)
plt.title('Angular Position vs Time')
plt.ylabel('Angular Position [deg]')
plt.xlabel('Time [s]')

plot2 = plt.figure(2)
plt.plot(t[1:len(t)-1],vel)
plt.title('Angular Velocity vs Time')
plt.ylabel('Angular Velocity [deg/s]')
plt.xlabel('Time [s]')
#plt.ylim(0, 500) 
#plt.xlim(1644557720,1644557750)
plt.show()
    
