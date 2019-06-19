#!/usr/bin/python3
import serial
import time
 
puerto   = serial.Serial(port = 'COM5',
                         baudrate = 115200,
                         bytesize = serial.EIGHTBITS,
                         parity   = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE)
 
try:
    puerto.write('0'.encode())
    time.sleep(1)
    puerto.write('1'.encode())

    getSerialValue = puerto.readline()
    print ('\nRx: %s'%(getSerialValue))

    puerto.close()
 
except serial.SerialException:
    print('Port is not available') 
 
except serial.portNotOpenError:
    print('Attempting to use a port that is not open')
    print('End of script') 