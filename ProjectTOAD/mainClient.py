import serial
import os
import time
    

ser = serial.Serial('COM10',baudrate = 9600,timeout = 1)
time.sleep(1)
pathName = 'C:/Users/spong/Documents/ProjectTOAD/SampleFiles'
n = 1
fileName = 'samples{}.txt'.format(n)
completeName = os.path.join(pathName,fileName)
newFile = open(completeName,"w")
newFile.write("Time,EncoderAngle")
newFile.write("\n")
while 1:
    while(ser.inWaiting()==0):
        pass
    dataPacket = str(ser.readline(),'utf-8')
    t = time.time()
    dataPacket = dataPacket.strip('\r\n')
    newFile.write(str(t))
    newFile.write(",")
    newFile.write(str(dataPacket))
    newFile.write("\n")
    print(dataPacket)
    print(t)