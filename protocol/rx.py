import serial
import crc8
import time
ser = serial.Serial('COM4',115200,timeout=5)
frameNO = 0
tranRe = False
reAck = False
frameACK = 0
data =""
def crc(data):
    hash = crc8.crc8()
    hash.update(bytes([data]))
    return hash.hexdigest()
def ctrl(num):
    if num == 0 :
        getCtrl = 0
    elif num == 1 :
        getCtrl = 1
    elif num == 2 :
        getCtrl = 2
    elif num == 3 :
        getCtrl = 3
    return getCtrl
def sendACK_t(frameNO):
    frame = 0
    frame <<= 2
    frame |= ctrl(frameNO)
    frame <<= 4
    frame |= 0
    frame <<= 8
    frame |= int(crc(0), 16)
    frame = str(frame)
    for i in range(len(frame)):
        ser.write(frame[i].encode())
        
def sendACK(frameNO):
    frame = 0
    frame <<= 2
    frame |= ctrl(frameNO)
    frame <<= 4
    frame |= int(data)
    frame <<= 8
    frame |= int(crc(data + frameNO), 16)
    print(frame)
    frame = str(frame)
    for i in range(len(frame)):
        ser.write(frame[i].encode())

def sendFrame(frameACK):
        sendACK(frameACK) #send frame
        ser.write(b';')
def read():
    b = ""
    b = ser.read(1)
    b = b.decode()
    if len(b) == 0:
        read()
    else :
        return b

while 1:
    if tranRe :
        if frameNO == 0:
            ser.write(b';')
            time.sleep(0.5)
            sendACK_t(3)
            print("ACK 3")

            
        if frameNO == 1:
            ser.write(b';')
            time.sleep(0.5)
            sendACK_t(2)
            print("ACK 2")

        c= ""
        c = ser.read(5)
        c = c.decode()
        if len(c) >= 3 :
            data2 = bin(int(data, 10))[2:].zfill(4)
            if data2[2] == '0' and data2[3] == '1':
                ser.write(b'1')
            if data2[2] == '1' and data2[3] == '0':
                ser.write(b'2')
            if data2[2] == '1' and data2[3] == '1':
                ser.write(b'3')
            time.sleep(0.5) 
            ser.write(b';')  #read
            time.sleep(0.5)
            b = read()  ####### รอรับค่าขนาดภาพ b = 1,2,3
            data = bin(int(data, 10))[2:].zfill(4)
            time.sleep(0.5)
            ser.write(b';')
            sendFrame(frameACK)
            # read
            tranRe = False
            reAck = True
    else :
        if reAck == False :
            a =""
            a = ser.read(5)
            a = a.decode()
            print(a,len(a))
            if len(a)<3 or a == '\r':
                tranRe = False
            else :
                a = str(a)
                bi = bin(int(a, 10))[2:].zfill(14)
                print("bi :",bi)
                frameNO = int(bi[0:2],2)
                oldCrc = bi[6:]
                data = bi[2:6]
                data = int(data,2)
                print(bin(int(crc(data), 16))[2:].zfill(8),oldCrc)
                if bin(int(crc(data), 16))[2:].zfill(8) == oldCrc :
                    print(data)
                    print(crc(data))
                    tranRe = True
                    data = str(data)
                    
                else:
                    tranRe = False
############### check ACK ตอนเราส่ง frame ขนาดรูป 
        elif reAck == True:
            a= ""
            a = ser.read(5)
            a = a.decode()
            if len(a)<3 :
                ser.write(b';') #write
                sendFrame(frameACK)
                # read in function
            else :
                a = str(a)
                bi = bin(int(a, 10))[2:].zfill(14)
                frameNO = int(bi[0:2],2)
                oldCrc = bi[6:]
                data = bi[2:6]
                data = int(data,2)
                if bin(int(crc(data), 16))[2:].zfill(8) == oldCrc :
                    print(data)
                    print(crc(data))
                    frameACK += 1
                    if frameACK >1:
                        frameACK = 0
                    reAck = False
                    
                else:
                    ser.write(b';')
                    sendFrame(frameACK)                
                


