import serial
import time


ser = serial.Serial('COM3', 38400, timeout=0,
                 parity=serial.PARITY_NONE, rtscts=1)
s = ser.read(100)       # read up to one hundred bytes
                         # or as much is in the buffer
print(s)


while True:
    s = ser.read(100)
    if s!=b'':
        print(s)
    time.sleep(0.5)