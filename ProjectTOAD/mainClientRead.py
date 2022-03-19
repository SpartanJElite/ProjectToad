import matplotlib.pyplot as plt
import os
import csv

pathName = 'C:/Users/spong/Documents/ProjectTOAD/SampleFiles'
n = 1
fileName = 'samples{}.txt'.format(n)
completeName = os.path.join(pathName,fileName)
time = []
angle = []
vel = []
enableCounter = 0
enableSkip = 2
with open(completeName,'r') as f:
    csvReader = csv.reader(f)
    for line in csvReader:
        if(enableCounter == enableSkip):
            time.append(float(line[0]))
            angle.append(float(line[1]))
        else:
            enableCounter = enableCounter + 1

for i in range(1,len(time)-1):
    vtemp = (angle[i+1]-angle[i-1])/(time[i+1]-time[i-1])
    vel.append(vtemp)

plot1 = plt. figure(1)
plt.plot(time,angle)
plt.title('Angular Position vs Time')
plt.ylabel('Angular Position [deg]')
plt.xlabel('Time [s]')

plot2 = plt.figure(2)
plt.plot(time[1:len(time)-1],vel)
plt.title('Angular Velocity vs Time')
plt.ylabel('Angular Velocity [deg/s]')
plt.xlabel('Time [s]')
plt.ylim(0, 500) 
plt.xlim(1644557720,1644557750)
plt.show()



