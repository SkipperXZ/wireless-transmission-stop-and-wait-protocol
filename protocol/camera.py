import cv2
import os
import serial
import time

smallsize = 15000
mediumsize = 30000
bigsize = 45000

# your Serial port should be different!
arduino = serial.Serial('COM9', 115200)
#cam = serial.Serial('COM1',115200)

def captureCircle():
    size = 0
    #sleep for a the time to capture image
    time.sleep(7)
    #  
    items = os.listdir('c:\out')
    num2 = 0
    for name in items:
        num, tmp = name.split(".bmp")
        num = int(num)
        num = max(num, num2)
        num2 = num

    img = cv2.imread("C:/out/"+str(num2)+".bmp")
    
    cb=0
    cw=0
    xx=img.shape[0]
    yy=img.shape[1]
    for i in range(0,xx):
        for j in range(0,yy):
            if img[i,j,2]< 50:
                cb+=1
            if img[i,j,2]>100:
                cw+=1
    print("Black : ",cb," White : ",cw)
    if cb > bigsize:
        size = 1
    elif cb > mediumsize:
        size = 2
    elif cb > smallsize:
        size = 3
    return str(size)

while True:
    a = input()
    arduino.write(a.encode())
    if(a == "q"):
        break
    print("size of cb ",captureCircle())