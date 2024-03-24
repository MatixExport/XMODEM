import serial.tools.list_ports as port_list
import serial

ports = list(port_list.comports())
for p in ports:
    print (p)


ser = serial.Serial('COM2')  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'hello')     # write a string
ser.close()             # close port



