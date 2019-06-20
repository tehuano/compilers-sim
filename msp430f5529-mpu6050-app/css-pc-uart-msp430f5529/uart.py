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

# Handshake...
ok = b''
while ok.strip() != b'0':
    port.write(b"1")
    ok = port.read()
    #print(ok.strip())
    Th = port.read(2) 
 #   Tl = port.read()[0]
    Axh = port.read(2)
 #   Axl = port.read()[0]
    Ayh = port.read(2)
 #   Ayl = port.read()[0]
    Azh = port.read(2)
  #  Azl = port.read()[0]
    Gxh = port.read(2)
 #   Gxl = port.read()[0]
    Gyh = port.read(2)
#    Gyl = port.read()[0]
    Gzh = port.read(2)
 #   Gzl = port.read()[0]
    Temp = int.from_bytes(Th,byteorder = 'big')
    Ax = (int.from_bytes(Axh,byteorder = 'big', signed = True)) / 131
    Ay = (int.from_bytes(Ayh,byteorder = 'big', signed = True)) / 131
    Az = (int.from_bytes(Azh,byteorder = 'big', signed = True)) / 131
    Gx = (int.from_bytes(Gxh,byteorder = 'big', signed = True)) / 16384
    Gy = (int.from_bytes(Gyh,byteorder = 'big', signed = True)) / 16384
    Gz = (int.from_bytes(Gzh,byteorder = 'big', signed = True)) / 16384
    print("T = {} | Ax = {}, Ay = {}, Az = {} | Gx = {}, Gy = {}, Gz = {}".format(Temp,Ax,Ay,Az,Gx,Gy,Gz))
	
port.close()