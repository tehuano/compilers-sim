#!/usr/bin/python3
import serial
import time
 
print("Connecting to serial port ...")
port = serial.Serial(port = 'COM5',
                     baudrate = 115200,
                     #baudrate = 9600,
                     bytesize = serial.EIGHTBITS,
                     parity   = serial.PARITY_NONE,
                     stopbits = serial.STOPBITS_ONE,
                     timeout=1)
print("Connected!!")

while True:
    # Handshake...
    ok = b''
    while ok.strip() != b'0':
        port.write(b"1")
        ok = port.read()
        #print(ok.strip())
    Th = port.read()[0]
    Tl = port.read()[0]
    Axh = port.read()[0]
    Axl = port.read()[0]
    Ayh = port.read()[0]
    Ayl = port.read()[0]
    Azh = port.read()[0]
    Azl = port.read()[0]
    Gxh = port.read()[0]
    Gxl = port.read()[0]
    Gyh = port.read()[0]
    Gyl = port.read()[0]
    Gzh = port.read()[0]
    Gzl = port.read()[0]
    Temp = ((Th << 8) | Tl) & 0xffff
    Ax = ((Axh << 8) | Axl) & 0xffff
    Ay = ((Ayh << 8) | Ayl) & 0xffff
    Az = ((Azh << 8) | Azl) & 0xffff
    Gx = ((Gxh << 8) | Gxl) & 0xffff
    Gy = ((Gyh << 8) | Gyl) & 0xffff
    Gz = ((Gzh << 8) | Gzl) & 0xffff
    print("T = {} | Ax = {}, Ay = {}, Az = {} | Gx = {}, Gy = {}, Gz = {}".format(Temp,Ax,Ay,Az,Gx,Gy,Gz))
        
port.close()
