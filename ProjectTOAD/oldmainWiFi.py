from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import matplotlib.pyplot as plt

def getNumbers(text):
    nums = []
    counter = 0
    for i in range(0,len(text)):
        num = text[i]
        if((num.isnumeric()==True)or(num == '.')):
            x = True
        else:
            x = False
        if((x == True)and(counter == 0)):
            counter = 1
            temp = []
            temp.append(num)
        elif((x == True)and(i == (len(text)-1))):
            temp.append(num)
            y = float(''.join(temp))
            nums.append(y)
            counter = 0
        elif((x == True)and(counter == 1)):
            temp.append(num)
        elif((x == False)and(counter == 1)):
            y = float(''.join(temp))
            nums.append(y)
            counter = 0
    return nums

def array2(arry):
    val = []
    t = []
    for i in range(0,len(arry)):
        if ((i%2) == 0):
            val.append(arry[i])
        elif((i%2) == 1):
            t.append(arry[i]/1000)
    return val,t

def velocity(val,t):
    vel = []
    for i in range(1,len(t)-1):
        vtemp = (val[i+1]-val[i-1])/(val[i+1]-val[i-1])
        vel.append(vtemp)
    return vel

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("http://172.20.10.4/")

#main = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.ID,"main")))
main = driver.find_element_by_id("main")
nums = getNumbers(main.text)
driver.quit()
[val,t] = array2(nums)
print(val)
print(t)
vel = velocity(val,t)

plot1 = plt. figure(1)
plt.plot(t,val)
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