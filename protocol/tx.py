import serial
import crc8
from time import sleep
ser = serial.Serial('COM7',115200,timeout=5)
frameNO = 0
ackNO = 3
tranRe = True
frameAck = True

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
def sendFrame(frameNO,data):
    frame = 0
    frame <<= 2
    frame |= ctrl(frameNO)
    frame <<= 4
    frame |= int(data)
    frame <<= 8
    frame |= int(crc(data + frameNO), 16)
    print("Sent frame : ",frame)
    frame = str(frame)
    for i in range(len(frame)):
        ser.write(frame[i].encode())
    ser.write(b';')
def sendACK(frameNO):
    data = 0
    frame = 0
    frame <<= 2
    frame |= ctrl(frameNO)
    frame <<= 4
    frame |= int(data)
    frame <<= 8
    frame |= int(crc(data + frameNO), 16)
    print("Sent ACK : ",frame)
    frame = str(frame)
    for i in range(len(frame)):
        ser.write(frame[i].encode())
    ser.write(b';')
while 1:
    if tranRe :
        if frameAck:
            data = int(input())
            sendFrame(frameNO,data)
        else :
            sendACK(ackNO)
            frameAck = True
        tranRe = False
    else :
        a = ''
        try:
            print("Waiting for data")
            a = ser.read(5).decode()  # receive ack
        except:
            print("invalid ack")
        if len(a)<3 :
            print("ACK lost")
            ser.write(b';')
            sendFrame(frameNO,data)
            lost = True
        else :
            if(a == '\r\n\r\n\r' or a == '\n\r\n' or a == '\n\r\n$2'):
                print("DEAD")
                pass
            else:
                rec = int(a)
                print("Frame : ", a)
                temp = rec & 255
                print("CRC : ", temp)
                rec >>= 8
                frame = rec & 31
                data = rec & 15
                print("Data = ", data)
                rec >>= 4
                recNO = rec
                print("Receive Frame NO : ", rec)
                if ackNO == recNO :
                    if int(crc(frame),16) == temp :
                        if data == 0:
                            print("Receive ACK")
                            frameNO = recNO-2
                            ser.write(b';')
                            data = int(input())
                            sendFrame(frameNO,data)
                        else:
                            ser.write(b';')
                            sendACK(ackNO)
                        print('X')
                    else:
                        ser.write(b';')
                        sendACK(ackNO)
                        print("CRC GAME")
                else :
                    print("ACK GAME")
                    ser.write(b';')
                    sendACK(ackNO)
        if lost :
            pass
        else:
            frameNO += 1;
            if frameNO > 1 : frameNO = 0
            frameAck = False
            tranRe = True
            lost = False
        ackNO += 1
        if ackNO > 3: ackNO = 2
