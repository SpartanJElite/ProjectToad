import numpy as np
import math
from vpython import *
from time import *
import serial
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

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

def writeCSV(t,ySol):
    pathName = 'C:/Users/spong/Documents/ProjectTOAD/SampleFiles'
    fileName = 'samples8.txt'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,"w")
    newFile.write("Time,EulerAngle1,EulerAngle2,EulerAngle3")
    newFile.write("\n")
    for i in range(0,len(t)):
        newFile.write(str(t[i]))
        newFile.write(",")
        newFile.write(str(ySol[i,0]))
        newFile.write(",")
        newFile.write(str(ySol[i,1]))
        newFile.write(",")
        newFile.write(str(ySol[i,2]))
        newFile.write("\n")
    newFile.close()

def velocityFunc(val,t):
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

    

#VPYTHON STFF


toRad=2*np.pi/360
toDeg=1/toRad

# scene.range=5
# scene.forward=vector(-1,-1,-1)
 
# scene.width=600
# scene.height=600
 
# xarrow=arrow(lenght=2, shaftwidth=.1, color=color.red,axis=vector(3,0,0),pos=vector(0,0,0))
# yarrow=arrow(lenght=2, shaftwidth=.1, color=color.green,axis=vector(0,3,0),pos=vector(0,0,0))
# zarrow=arrow(lenght=4, shaftwidth=.1, color=color.blue,axis=vector(0,0,3),pos=vector(0,0,0))
# frontArrow=arrow(length=4,shaftwidth=.1,color=color.purple,axis=vector(1,0,0),pos=vector(0,0,0))
# upArrow=arrow(length=1,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0),pos=vector(0,0,0))
# sideArrow=arrow(length=2,shaftwidth=.1,color=color.orange,axis=vector(0,0,1),pos=vector(0,0,0))
# mainbody=cylinder(radius=1,axis=vector(3,0,0),opacity=.8,pos=vector(-1.5,0,0))
# nozzle1=cylinder(radius=0.2,axis=vector(0.25,0,0),opacity=.8,pos=vector(-1.75,0.5,0),color=color.blue)
# mainbody.rotate(angle=np.pi/2)
# nozzle2=cylinder(radius=0.2,axis=vector(0.25,0,0),opacity=.8,pos=vector(-1.75,-0.5,0),color=color.blue)
# nozzle3=cylinder(radius=0.2,axis=vector(0.25,0,0),opacity=.8,pos=vector(-1.75,0,0.5),color=color.blue)
# nozzle4=cylinder(radius=0.2,axis=vector(0.25,0,0),opacity=.8,pos=vector(-1.75,0,-0.5),color=color.blue)
# nozzle5=cylinder(radius=0.2,axis=vector(0.25,0,0),opacity=.8,pos=vector(-1.75,0,0),color=color.blue)
# myObj=compound([mainbody,nozzle1,nozzle2,nozzle3,nozzle4,nozzle5])

w = [0,1,1]
yaw = 0 *toRad
pitch = 0 *toRad
roll = 0 *toRad
quat = angle2quat(yaw,pitch,roll)
t = np.linspace(0,60,6001)
ySol = odeint(odes,quat,t,args=(w,))
ySol = array_quat2eul(ySol)

dySolx = velocityFunc(ySol[:,0],t)
dySoly = velocityFunc(ySol[:,1],t)
dySolz = velocityFunc(ySol[:,2],t)
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

# writeCSV(t,ySol)
# t = range(1,500,1)

# for j in range(0,len(t)):
#    roll = ySol[j,2]*toRad
   
#    pitch = ySol[j,1]*toRad
#    yaw = ySol[j,0]*toRad
#    print("Roll=",roll*toDeg," Pitch=",pitch*toDeg,"Yaw=",yaw*toDeg)
#    rate(50)
#    k=vector(cos(yaw)*cos(pitch), sin(pitch),sin(yaw)*cos(pitch))
#    y=vector(0,1,0)
#    s=cross(k,y)
#    v=cross(s,k)
#    vrot=v*cos(roll)+cross(k,v)*sin(roll) 
#    frontArrow.axis=k
#    sideArrow.axis=cross(k,vrot)
#    upArrow.axis=vrot
#    myObj.axis=k
#    myObj.up=vrot
#    sideArrow.length=3
#    frontArrow.length=3
#    upArrow.length=3